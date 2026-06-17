import asyncio
import httpx
from datetime import datetime
from nicegui import ui

BASE_URL = "http://localhost:8000"
PING_HOST = "192.168.12.2"


# ─── Shared helper functions ──────────────────────────

async def fetch_tests(endpoint: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{endpoint}")
        return response.json()


async def start_run(endpoint: str, payload: dict):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/{endpoint}", json=payload)


async def check_ping(host: str, timeout: int = 2) -> bool:
    """Ping the host once with a timeout. Returns True if host responds."""
    import subprocess

    def _ping():
        try:
            cmd = ["ping", "-c", "1", "-W", str(timeout), host]
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0
        except Exception:
            return False

    return await asyncio.to_thread(_ping)


async def poll_status(endpoint: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{endpoint}")
        return response.json()


async def stop_run(endpoint: str):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/{endpoint}")


def format_duration(seconds: float | None) -> str:
    if seconds is None:
        return ""
    total = int(seconds)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02}:{m:02}:{s:02}"


def format_rows(rows: list[dict]) -> list[dict]:
    return [
        {**r, "duration": format_duration(r.get("duration"))} for r in rows
    ]

def apply_preset(preset: list[str], dvt_checkboxes: dict, dvt_flows: dict, dvt_flow_toggles: dict):
    # Uncheck all first
    for cb in dvt_checkboxes.values():
        cb.set_value(False)
    for toggle in dvt_flow_toggles.values():
        toggle.set_value(False)

    # Check only preset tests
    for test in preset:
        if test in dvt_checkboxes:
            dvt_checkboxes[test].set_value(True)

    # Enable flow toggles where all tests in that flow are selected
    for flow_name, flow_tests in dvt_flows.items():
        if all(t in preset for t in flow_tests):
            dvt_flow_toggles[flow_name].set_value(True)


def make_table_columns():
    return [
        {"name": "name",        "label": "Test",        "field": "name",        "align": "center", "style": "width: 100px; white-space: normal; word-break: break-word;"},
        {"name": "command",     "label": "Command",     "field": "command",     "align": "center", "style": "width: 400px; white-space: normal; word-break: break-word;"},
        {"name": "status",      "label": "Status",      "field": "status",      "align": "center", "style": "width: 100px; white-space: normal;"},
        {"name": "duration",    "label": "Test Time",   "field": "duration",    "align": "center", "style": "width: 100px; white-space: normal;"},
        {"name": "output_path", "label": "Result Path", "field": "output_path", "align": "center", "style": "width: 200px; white-space: normal; word-break: break-all;"},
    ]


def make_table(columns: list) -> ui.table:
    table = ui.table(columns=columns, rows=[]).classes("w-full").style("table-layout: fixed;")
    table.add_slot("body-cell-status", """
        <q-td :props="props" style="text-align: center;">
            <q-badge
                :color="props.value === 'pass' ? 'green' : props.value === 'fail' ? 'red' : 'grey'"
                :label="props.value"
                style="font-size: 12px; padding: 4px 10px;"
            />
        </q-td>
    """)
    table.add_slot("body-cell-output_path", """
        <q-td :props="props">
            <span v-if="props.value" style="font-size: 11px; color: grey; word-break: break-all;">
                {{ props.value }}
            </span>
            <span v-else style="font-size: 12px; color: grey;">—</span>
        </q-td>
    """)
    return table


async def run_polling_loop(
    poll_endpoint: str,
    results_table: ui.table,
    summary_label: ui.label,
    status_label: ui.label,
    timer_label: ui.label,
    run_btn: ui.button,
    stop_btn: ui.button,
):
    start_time = None

    while True:
        data = await poll_status(poll_endpoint)

        # Start the total timer when the first test actually begins running
        running = next((r for r in data["results"] if r["status"] == "running"), None)
        if running and start_time is None:
            start_time = datetime.now()

        elapsed = 0 if start_time is None else int((datetime.now() - start_time).total_seconds())
        timer_label.set_text(f"Total test time: {format_duration(elapsed)}")

        if running:
            status_label.set_text(f"Running: {running['name']}...")

        if data["status"] in ("done", "error", "stopped"):
            if data["status"] == "stopped":
                await asyncio.sleep(0.5)
                data = await poll_status(poll_endpoint)

            results_table.rows[:] = format_rows(data["results"])
            results_table.update()
            summary_label.set_text(data["summary"])
            status_label.set_text(
                "✅ Done"    if data["status"] == "done"    else
                "⛔ Stopped" if data["status"] == "stopped" else
                "❌ Error"
            )
            final_elapsed = 0 if start_time is None else int((datetime.now() - start_time).total_seconds())
            timer_label.set_text(f"Total test time: {format_duration(final_elapsed)}")
            run_btn.enable()
            stop_btn.disable()
            break

        results_table.rows[:] = format_rows(data["results"])
        results_table.update()

        await asyncio.sleep(1)


# ─── Page ─────────────────────────────────────────────

@ui.page("/")
async def index():

    # ─── Fetch tests for both tabs ────────────────────
    bft_available_tests = await fetch_tests("bft/tests")
    dvt_available_tests = await fetch_tests("dvt/tests")

    with ui.card().classes("w-full"):
        ui.label("Harmony Test Dashboard").classes("text-xl font-bold")

        with ui.tabs() as tabs:
            bft_tab = ui.tab("BFT")
            dvt_tab = ui.tab("DVT")

        with ui.tab_panels(tabs, value=bft_tab).classes("w-full"):

            # ─────────────────────────────────────────
            # BFT TAB
            # ─────────────────────────────────────────
            with ui.tab_panel(bft_tab):
                bft_checkboxes: dict[str, ui.checkbox] = {}

                bft_serial_input = ui.input(label="Board Serial Number")

                async def handle_bft_run():
                    if not bft_serial_input.value.strip():
                        ui.notify("Please enter a serial number", type="warning", position="top")
                        return

                    if bft_run_all_toggle.value:
                        selected = bft_available_tests
                    else:
                        selected = [name for name, cb in bft_checkboxes.items() if cb.value]
                        if not selected:
                            ui.notify("Please select at least one test", type="warning", position="top")
                            return

                    bft_run_btn.disable()
                    bft_stop_btn.enable()
                    bft_status_label.set_text("Running...")
                    bft_timer_label.set_text("Total test time: 00:00:00")
                    bft_results_table.rows.clear()
                    bft_results_table.update()
                    bft_summary_label.set_text("")

                    # Run a ping test until the DUT responds (mirrors ping_test.py output)
                    bft_status_label.set_text(f"Monitoring {PING_HOST}. Waiting for response...")
                    attempt = 1
                    delay_seconds = 2
                    while True:
                        ok = await check_ping(PING_HOST)
                        if ok:
                            bft_status_label.set_text(f"✅ Success! {PING_HOST} responded on attempt {attempt}. Starting tests...")
                            break
                        else:
                            bft_status_label.set_text(f"Attempt {attempt}: Host is still down. Retrying in {delay_seconds}s...")
                            attempt += 1
                            await asyncio.sleep(delay_seconds)

                    await start_run("run", {
                        "serial_no": bft_serial_input.value.strip(),
                        "tests": selected
                    })

                    await run_polling_loop(
                        poll_endpoint="run/current",
                        results_table=bft_results_table,
                        summary_label=bft_summary_label,
                        status_label=bft_status_label,
                        timer_label=bft_timer_label,
                        run_btn=bft_run_btn,
                        stop_btn=bft_stop_btn,
                    )

                async def handle_bft_stop():
                    await stop_run("stop")
                    
                with ui.row():
                    bft_run_btn  = ui.button("Run",  on_click=handle_bft_run)
                    bft_stop_btn = ui.button("Stop", on_click=handle_bft_stop).props("color=red")
                    bft_stop_btn.disable()

                with ui.row().classes("items-center gap-4"):
                    ui.label("Run All")
                    bft_run_all_toggle = ui.switch(value=True)

                with ui.column():
                    for test in bft_available_tests:
                        bft_checkboxes[test] = ui.checkbox(test, value=True)

                def on_bft_toggle_change():
                    if bft_run_all_toggle.value:
                        for cb in bft_checkboxes.values():
                            cb.set_value(True)
                    else:
                        for cb in bft_checkboxes.values():
                            cb.set_value(False)

                bft_run_all_toggle.on_value_change(on_bft_toggle_change)

                bft_summary_label = ui.label("").classes("text-sm text-gray-500")
                bft_status_label  = ui.label("").classes("text-sm")
                bft_timer_label   = ui.label("").classes("text-sm text-gray-400")
                bft_results_table = make_table(make_table_columns())
                
            # ─────────────────────────────────────────
            # DVT TAB
            # ─────────────────────────────────────────
            with ui.tab_panel(dvt_tab):
                dvt_checkboxes: dict[str, ui.checkbox] = {}
                dvt_flow_toggles: dict[str, ui.switch] = {}

                dvt_serial_input = ui.input(label="Board Serial Number")

                dvt_temp = ui.select(
                    label="Temp",
                    options=["25c", "60c", "-45c"],
                    value="25c"
                ).classes("w-32")

                async def handle_dvt_run():
                    if not dvt_serial_input.value.strip():
                        ui.notify("Please enter a serial number", type="warning", position="top")
                        return

                    selected = [name for name, cb in dvt_checkboxes.items() if cb.value]
                    if not selected:
                        ui.notify("Please select at least one test", type="warning", position="top")
                        return

                    # ── Countdown if scheduled ────────
                    if dvt_schedule_toggle.value:
                        try:
                            h, m, s = map(int, dvt_schedule_time.value.strip().split(":"))
                            delay = h * 3600 + m * 60 + s
                        except ValueError:
                            ui.notify("Invalid time format. Use HH:MM:SS", type="warning", position="top")
                            return

                        if delay > 0:
                            dvt_schedule_cancelled["value"] = False  # reset flag
                            dvt_run_btn.disable()
                            dvt_stop_btn.disable()
                            dvt_cancel_btn.set_visibility(True)      # show cancel button
                            remaining = delay

                            while remaining > 0:
                                if dvt_schedule_cancelled["value"]:  # check flag each tick
                                    return                            # abort the run entirely
                                dvt_countdown_label.set_text(f"Starting in: {format_duration(remaining)}")
                                await asyncio.sleep(1)
                                remaining -= 1

                            dvt_cancel_btn.set_visibility(False)     # hide when countdown ends
                            dvt_countdown_label.set_text("")

                    # Show only tables for flows that have selected tests
                    for flow_name in dvt_flows.keys():
                        has_tests = any(t in selected for t in dvt_flows[flow_name])
                        dvt_flow_sections[flow_name].set_visibility(has_tests)
                        dvt_flow_tables[flow_name].rows.clear()
                        dvt_flow_tables[flow_name].update()

                    dvt_run_btn.disable()
                    dvt_stop_btn.enable()
                    dvt_status_label.set_text("Running...")
                    dvt_timer_label.set_text("Total test time: 00:00:00")
                    dvt_summary_label.set_text("")

                    # Run a ping test until the DUT responds (mirrors ping_test.py output)
                    dvt_status_label.set_text(f"Monitoring {PING_HOST}. Waiting for response...")
                    attempt = 1
                    delay_seconds = 2
                    while True:
                        ok = await check_ping(PING_HOST)
                        if ok:
                            dvt_status_label.set_text(f"✅ Success! {PING_HOST} responded on attempt {attempt}. Starting tests...")
                            break
                        else:
                            dvt_status_label.set_text(f"Attempt {attempt}: Host is still down. Retrying in {delay_seconds}s...")
                            attempt += 1
                            await asyncio.sleep(delay_seconds)

                    await start_run("dvt/run", {
                        "serial_no": dvt_serial_input.value.strip(),
                        "temperature": dvt_temp.value,
                        "tests": selected
                    })

                    start_time = None

                    def group_by_flow(results: list) -> dict[str, list]:
                        flow_results: dict[str, list] = {f: [] for f in dvt_flows.keys()}
                        for r in results:
                            flow = r.get("flow") or "Unknown"
                            if flow in flow_results:
                                flow_results[flow].append(r)
                        return flow_results

                    def update_flow_tables(flow_results: dict[str, list]):
                        for flow_name, rows in flow_results.items():
                            if rows:
                                dvt_flow_tables[flow_name].rows[:] = format_rows(rows)
                                dvt_flow_tables[flow_name].update()

                    while True:
                        data = await poll_status("dvt/run/current")

                        # Start timer when first test reports 'running'
                        running = next((r for r in data["results"] if r["status"] == "running"), None)
                        if running and start_time is None:
                            start_time = datetime.now()

                        elapsed = 0 if start_time is None else int((datetime.now() - start_time).total_seconds())
                        dvt_timer_label.set_text(f"Total test time: {format_duration(elapsed)}")

                        if running:
                            dvt_status_label.set_text(f"Running: {running['name']}...")

                        update_flow_tables(group_by_flow(data["results"]))

                        if data["status"] in ("done", "error", "stopped"):
                            if data["status"] == "stopped":
                                await asyncio.sleep(0.5)
                                data = await poll_status("dvt/run/current")
                                update_flow_tables(group_by_flow(data["results"]))

                            dvt_summary_label.set_text(data["summary"])
                            dvt_status_label.set_text(
                                "✅ Done"    if data["status"] == "done"    else
                                "⛔ Stopped" if data["status"] == "stopped" else
                                "❌ Error"
                            )
                            final_elapsed = 0 if start_time is None else int((datetime.now() - start_time).total_seconds())
                            dvt_timer_label.set_text(f"Total test time: {format_duration(final_elapsed)}")
                            dvt_run_btn.enable()
                            dvt_stop_btn.disable()
                            break

                        await asyncio.sleep(1)

                async def handle_dvt_stop():
                    await stop_run("dvt/stop")

                dvt_schedule_cancelled = {"value": False}  # mutable flag

                async def handle_dvt_cancel_schedule():
                    dvt_schedule_cancelled["value"] = True
                    dvt_countdown_label.set_text("")
                    dvt_run_btn.enable()
                    dvt_cancel_btn.set_visibility(False)

                with ui.row().classes("items-center gap-4"):
                    dvt_run_btn  = ui.button("Run",  on_click=handle_dvt_run)
                    dvt_stop_btn = ui.button("Stop", on_click=handle_dvt_stop).props("color=red")
                    dvt_cancel_btn = ui.button("Cancel Schedule", on_click=handle_dvt_cancel_schedule).props("color=orange")
                    dvt_stop_btn.disable()
                    dvt_cancel_btn.set_visibility(False)

                # ── Scheduled start ───────────────────
                with ui.row().classes("items-center gap-4 mt-2"):
                    ui.label("Schedule Start").classes("text-sm")
                    dvt_schedule_toggle = ui.switch(value=False)
                    dvt_schedule_time   = ui.input(
                        label="Start after (HH:MM:SS)",
                        value="00:00:00"
                    ).classes("w-40")
                    dvt_schedule_time.set_visibility(False)

                dvt_countdown_label = ui.label("").classes("text-sm text-orange-500")

                def on_schedule_toggle_change():
                    dvt_schedule_time.set_visibility(dvt_schedule_toggle.value)
                    if not dvt_schedule_toggle.value:
                        dvt_countdown_label.set_text("")

                dvt_schedule_toggle.on_value_change(on_schedule_toggle_change)               

                # Fetch flow structure from backend
                async with httpx.AsyncClient() as client:
                    dvt_flows: dict = (await client.get(f"{BASE_URL}/dvt/flows")).json()

                # ── Band-level RUN ALL toggles ────────
                with ui.row().classes("items-center gap-8 mb-2"):
                    ui.label("Run All 3GHz Flows").classes("font-medium")
                    run_all_3g = ui.switch(value=False)
                    ui.label("Run All 6GHz Flows").classes("font-medium")
                    run_all_6g = ui.switch(value=False)

                # ── Preset buttons ────────────────────
                with ui.row().classes("items-center gap-4 mb-2"):
                    async def handle_3ghz_reduced():
                        async with httpx.AsyncClient() as client:
                            preset = (await client.get(f"{BASE_URL}/dvt/presets/3ghz-reduced")).json()
                        apply_preset(preset, dvt_checkboxes, dvt_flows, dvt_flow_toggles)

                    async def handle_6ghz_reduced():
                        async with httpx.AsyncClient() as client:
                            preset = (await client.get(f"{BASE_URL}/dvt/presets/6ghz-reduced")).json()
                        apply_preset(preset, dvt_checkboxes, dvt_flows, dvt_flow_toggles)

                    ui.button("3GHz Reduced Flow", on_click=handle_3ghz_reduced).props("outline")
                    ui.button("6GHz Reduced Flow", on_click=handle_6ghz_reduced).props("outline")

                def apply_band_toggle(band_prefix: str, enable: bool):
                    for flow_name, toggle in dvt_flow_toggles.items():
                        if flow_name.startswith(band_prefix):
                            toggle.set_value(enable)
                            for test in dvt_flows[flow_name]:
                                dvt_checkboxes[test].set_value(enable)

                def on_run_all_3g_change():
                    apply_band_toggle("3GHz", run_all_3g.value)

                def on_run_all_6g_change():
                    apply_band_toggle("6GHz", run_all_6g.value)

                run_all_3g.on_value_change(on_run_all_3g_change)
                run_all_6g.on_value_change(on_run_all_6g_change)

                # ── Per-flow expansion with toggle ────
                for flow_name, flow_tests in dvt_flows.items():

                    with ui.row().classes("items-center gap-4 mt-1"):
                        flow_toggle = ui.switch(value=False)
                        dvt_flow_toggles[flow_name] = flow_toggle

                        with ui.expansion(flow_name).classes("flex-1"):
                            with ui.column():
                                for test in flow_tests:
                                    dvt_checkboxes[test] = ui.checkbox(test, value=False)

                    def make_toggle_handler(toggle, section_checkboxes):
                        def handler():
                            for cb in section_checkboxes:
                                cb.set_value(toggle.value)
                        return handler

                    section_cbs = [dvt_checkboxes[t] for t in flow_tests]
                    flow_toggle.on_value_change(make_toggle_handler(flow_toggle, section_cbs))

                dvt_summary_label = ui.label("").classes("text-sm text-gray-500")
                dvt_status_label  = ui.label("").classes("text-sm")
                dvt_timer_label   = ui.label("").classes("text-sm text-gray-400")
                
                # ── Per-flow result tables ────────────
                dvt_flow_tables: dict[str, ui.table] = {}
                dvt_flow_sections: dict[str, ui.column] = {}

                for flow_name in dvt_flows.keys():
                    with ui.column().classes("w-full") as flow_section:
                        flow_section.set_visibility(False)
                        ui.label(flow_name).classes("font-medium mt-4")
                        flow_table = make_table(make_table_columns())
                        dvt_flow_tables[flow_name] = flow_table
                        dvt_flow_sections[flow_name] = flow_section