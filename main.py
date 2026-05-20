import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Smart Ledger Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.padding = 0
    
    # --- सेफ स्टेट मॅनेजमेंट (क्रॅश-फ्री बॅकअपसह) ---
    backup_accounts = {}

    def get_accounts():
        try:
            if page.client_storage.contains_key("accounts"):
                data = page.client_storage.get("accounts")
                return data if isinstance(data, dict) else {}
            else:
                page.client_storage.set("accounts", {})
                return {}
        except Exception:
            # जर मोबाईल स्टोरेज उपलब्ध नसेल तर बॅकअप मेमरी वापरेल
            return backup_accounts

    def save_accounts(data):
        nonlocal backup_accounts
        try:
            page.client_storage.set("accounts", data)
        except Exception:
            pass
        backup_accounts = data

    # --- UI कंपोनंट्स व्याख्या ---
    in_display = ft.Text("₹0", size=20, weight="bold")
    out_display = ft.Text("₹0", size=20, weight="bold")
    people_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    detail_name = ft.Text("Name", weight="bold")
    summary_banner = ft.Container(ft.Text("Summary", weight="bold"), padding=15, border_radius=10, margin=15, alignment=ft.alignment.center)
    amt_input = ft.TextField(label="Amount (₹)", keyboard_type=ft.KeyboardType.NUMBER)
    note_input = ft.TextField(label="Note (Optional)")
    entry_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # --- लॉजिक फंक्शन्स ---
    
    def refresh_home():
        accounts = get_accounts()
        search_query = search_field.value.lower().strip() if search_field.value else ""
        
        people_list.controls.clear()
        total_in = 0
        total_out = 0

        for name, data in accounts.items():
            if not isinstance(data, dict):
                continue
            if search_query and search_query not in name.lower():
                continue
                
            entries = data.get('entries', [])
            balance = 0
            for e in entries:
                try:
                    amt = float(e.get('amount', 0))
                    balance += amt if e.get('type') == 'got' else -amt
                except (ValueError, TypeError):
                    continue
            
            if balance > 0: 
                total_in += balance
            elif balance < 0: 
                total_out += abs(balance)

            bal_color = ft.colors.BLUE if balance > 0 else ft.colors.RED if balance < 0 else ft.colors.GREY_700
            bal_text = "Settled" if balance == 0 else f"₹{abs(balance)}"
            sub_text = "YOU GET" if balance >= 0 else "YOU GIVE"

            # क्लीक इव्हेंट मधील लूप एरर टाळण्यासाठी सुरक्षित पद्धत
            def make_on_click(person_name):
                return lambda _: open_detail(person_name)

            people_list.controls.append(
                ft.ListTile(
                    title=ft.Text(name, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"{len(entries)} entries"),
                    trailing=ft.Column([
                        ft.Text(bal_text, color=bal_color, weight="bold"),
                        ft.Text(sub_text, size=10)
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment="end"),
                    on_click=make_on_click(name)
                )
            )
        
        in_display.value = f"₹{total_in}"
        out_display.value = f"₹{total_out}"
        try:
            page.update()
        except Exception:
            pass

    def open_detail(name):
        page.session.set("current_person", name)
        accounts = get_accounts()
        if name not in accounts: 
            return
            
        person = accounts[name]
        detail_name.value = name
        entries = person.get('entries', [])
        
        balance = 0
        for e in entries:
            try:
                balance += float(e['amount']) if e['type'] == 'got' else -float(e['amount'])
            except Exception:
                continue
        
        if balance > 0:
            summary_banner.content.value = f"You will get ₹{balance}"
            summary_banner.bgcolor = ft.colors.BLUE_50
            summary_banner.content.color = ft.colors.BLUE
        elif balance < 0:
            summary_banner.content.value = f"You will give ₹{abs(balance)}"
            summary_banner.bgcolor = ft.colors.RED_50
            summary_banner.content.color = ft.colors.RED
        else:
            summary_banner.content.value = "Account Settled"
            summary_banner.bgcolor = ft.colors.GREY_100
            summary_banner.content.color = ft.colors.GREY_700

        entry_list.controls.clear()
        for e in reversed(entries):
            is_got = e.get('type') == 'got'
            try:
                display_amt = float(e.get('amount', 0))
            except Exception:
                display_amt = 0
                
            entry_list.controls.append(
                ft.ListTile(
                    title=ft.Text(e.get('note', ''), size=14),
                    subtitle=ft.Text(e.get('date', ''), size=11),
                    trailing=ft.Text(
                        f"{'+' if is_got else '-'} ₹{display_amt}",
                        color=ft.colors.GREEN if is_got else ft.colors.RED,
                        weight="bold"
                    )
                )
            )
        
        home_view.visible = False
        detail_view.visible = True
        try:
            page.update()
        except Exception:
            pass

    def add_transaction(is_got):
        name = page.session.get("current_person")
        if not name: 
            return
            
        try:
            # इनपुट व्हॅलिडेशन (रिकामे किंवा चुकीचे शब्द टाकल्यास क्रॅश होणार नाही)
            clean_val = amt_input.value.strip() if amt_input.value else ""
            amt = float(clean_val)
            if amt <= 0: 
                return
        except (ValueError, TypeError): 
            return

        accounts = get_accounts()
        if name in accounts:
            if 'entries' not in accounts[name]:
                accounts[name]['entries'] = []
                
            accounts[name]['entries'].append({
                "amount": amt,
                "note": note_input.value.strip() if note_input.value else ("Cash Received" if is_got else "Payment Made"),
                "type": "got" if is_got else "gave",
                "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
            })
            
            save_accounts(accounts)
            amt_input.value = ""
            note_input.value = ""
            open_detail(name)

    def add_new_person(e):
        def close_dlg(ev):
            if name_field.value and name_field.value.strip():
                customer_name = name_field.value.strip()
                accounts = get_accounts()
                if customer_name not in accounts:
                    accounts[customer_name] = {"entries": []}
                    save_accounts(accounts)
                    refresh_home()
            dlg.open = False
            try:
                page.update()
            except Exception:
                pass

        name_field = ft.TextField(label="Customer Name", autofocus=True)
        dlg = ft.AlertDialog(
            title=ft.Text("Add Customer"),
            content=name_field,
            actions=[ft.TextButton("Add", on_click=close_dlg)]
        )
        page.dialog = dlg
        dlg.open = True
        try:
            page.update()
        except Exception:
            pass

    # --- लेआउट रचना ---
    search_field = ft.TextField(placeholder="Search customer...", on_change=lambda _: refresh_home())

    home_view = ft.Column([
        ft.Container(ft.Text("📝 Smart Ledger Pro", size=20, weight="bold"), padding=20, alignment=ft.alignment.center),
        ft.Row([
            ft.Container(ft.Column([ft.Text("YOU'LL GET", size=10), in_display]), bgcolor=ft.colors.BLUE_50, padding=15, border_radius=10, expand=True),
            ft.Container(ft.Column([ft.Text("YOU'LL GIVE", size=10), out_display]), bgcolor=ft.colors.RED_50, padding=15, border_radius=10, expand=True),
        ], spacing=10, padding=15),
        ft.Container(search_field, padding=ft.padding.only(left=15, right=15)),
        people_list
    ], expand=True)

    def back_to_home(_):
        detail_view.visible = False
        home_view.visible = True
        refresh_home()

    detail_view = ft.Column([
        ft.Row([
            ft.IconButton(ft.icons.ARROW_BACK, on_click=back_to_home),
            detail_name
        ], alignment="start"),
        summary_banner,
        ft.Container(ft.Column([
            amt_input, note_input,
            ft.Row([
                ft.ElevatedButton("GOT (+)", bgcolor=ft.colors.GREEN, color="white", on_click=lambda _: add_transaction(True), expand=True),
                ft.ElevatedButton("GAVE (-)", bgcolor=ft.colors.RED, color="white", on_click=lambda _: add_transaction(False), expand=True),
            ])
        ]), padding=15),
        ft.Container(ft.Text("TRANSACTION HISTORY", size=12, weight="bold", color=ft.colors.GREY_600), padding=ft.padding.only(left=15)),
        entry_list
    ], visible=False, expand=True)

    page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_new_person)
    page.add(home_view, detail_view)
    refresh_home()

ft.app(target=main)
