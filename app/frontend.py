import asyncio
import httpx
from datetime import datetime
from nicegui import ui

BASE_URL = "http://localhost:8000"


async def fetch_tests() -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/tests")
        return response.json()


async def start_run(serial_no: str, selected_tests: list[str]):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/run", json={
            "serial_no": serial_no,
            "tests": selected_tests
        })


async def poll_status() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/run/current")
        return response.json()


@ui.page("/")
async def index():
    available_tests = await fetch_tests()
    checkboxes: dict[str, ui.checkbox] = {}

    with ui.card().classes("w-full"):
        ui.label("BFT Dashboard").classes("text-xl font-bold")
        serial_input = ui.input(label="Serial Number")

        run_all = ui.toggle(["Run All", "Select"], value="Run All")

        with ui.column() as checkbox_section:
            for test in available_tests:
                checkboxes[test] = ui.checkbox(test)

        def on_toggle_change():
            checkbox_section.set_visibility(run_all.value == "Select")

        run_all.on_value_change(on_toggle_change)
        checkbox_section.set_visibility(False)

        columns = [
            {"name": "name",     "label": "Test",     "field": "name",     "align": "center", "style": "width: 100px; white-space: normal; word-break: break-word;"},
            {"name": "command",  "label": "Command",  "field": "command",  "align": "center", "style": "width: 400px; white-space: normal; word-break: break-word;"},
            {"name": "status",   "label": "Status",   "field": "status",   "align": "center", "style": "width: 100px; white-space: normal;"},
            {"name": "duration", "label": "Test time", "field": "duration", "align": "center", "style": "width: 100px; white-space: normal;"},
            {"name": "output_path", "label": "Results", "field": "output_path", "align": "center", "style": "width: 100px; white-space: normal;"}
        ]
                
        
        results_table = ui.table(columns=columns, rows=[]).classes("w-full").style("table-layout: fixed;")
        
        # To highlight pass/fail status with colors, we add a custom slot for the "status" column.
        results_table.add_slot("body-cell-status", """
        <q-td :props="props" style="text-align: center;">
            <q-badge
                :color="props.value === 'pass' ? 'green' : props.value === 'fail' ? 'red' : 'grey'"
                :label="props.value"
                style="font-size: 12px; padding: 4px 10px;"
            />
        </q-td>
        """)
        
        # Similarly, we can add a custom slot for the "output_path" column to display it as a clickable link if it exists, or a dash if it's null.
        # results_table.add_slot("body-cell-output_path", """
        # <q-td :props="props">
            
        #         v-if="props.value"
        #         :href="'file://' + props.value"
        #         target="_blank"
        #         style="font-size: 12px; color: var(--q-primary); word-break: break-all;"
        #     >
        #         {{ props.value }}
        #     </a>
        #     <span v-else style="color: grey; font-size: 12px;">—</span>
        # </q-td>
        # """)
        
        summary_label = ui.label("").classes("text-sm text-gray-500")
        status_label  = ui.label("").classes("text-sm")
        timer_label   = ui.label("").classes("text-sm text-gray-400")  # real time timer

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
                {**r, "duration": format_duration(r.get('duration'))} for r in rows
            ]

        async def handle_run():
            if not serial_input.value.strip():
                ui.notify("Please enter a serial number", type="warning", position="top")
                return

            if run_all.value == "Select":
                selected = [name for name, cb in checkboxes.items() if cb.value]
                if not selected:
                    ui.notify("Please select at least one test", type="warning", position="top")
                    return
            else:
                selected = available_tests

            run_btn.disable()
            stop_btn.enable()
            status_label.set_text("Running...")
            timer_label.set_text("Elapsed: 0s")
            results_table.rows.clear()
            results_table.update()
            summary_label.set_text("")

            await start_run(serial_input.value.strip(), selected)

            start_time = datetime.now()

            while True:
                data = await poll_status()

                # Update timer every tick
                elapsed = int((datetime.now() - start_time).total_seconds())
                timer_label.set_text(f"Elapsed: {format_duration(elapsed)}")

                if data["status"] in ("done", "error", "stopped"):
                    if data["status"] == "stopped":
                        await asyncio.sleep(0.5)
                        data = await poll_status()

                    results_table.rows[:] = format_rows(data["results"])
                    results_table.update()
                    summary_label.set_text(data["summary"])
                    status_label.set_text(
                        "✅ Done"    if data["status"] == "done"    else
                        "⛔ Stopped" if data["status"] == "stopped" else
                        "❌ Error"
                    )
                    # Show final elapsed time
                    final_elapsed = int((datetime.now() - start_time).total_seconds())
                    timer_label.set_text(f"Elapsed: {format_duration(final_elapsed)}")
                    run_btn.enable()
                    stop_btn.disable()
                    break

                results_table.rows[:] = format_rows(data["results"])
                results_table.update()

                running = next((r for r in data["results"] if r["status"] == "running"), None)
                if running:
                    status_label.set_text(f"Running: {running['name']}...")

                await asyncio.sleep(1)

        async def handle_stop():
            async with httpx.AsyncClient() as client:
                await client.post(f"{BASE_URL}/stop")

        with ui.row():
            run_btn  = ui.button("Run",  on_click=handle_run)
            stop_btn = ui.button("Stop", on_click=handle_stop).props("color=red")
            stop_btn.disable()