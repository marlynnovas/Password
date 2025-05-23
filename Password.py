import re
import flet as ft

def main(page: ft.Page):
    page.title = "🔐 Password Checker"
    page.window_width = 450
    page.window_height = 700
    page.bgcolor = ft.colors.PINK_50

    results = ft.Column(spacing=5)
    
    pwd_input = ft.TextField(
        label="Tu contraseña",
        password=True,
        width=350
    )

    eye_btn = ft.IconButton(
        icon=ft.icons.REMOVE_RED_EYE_OUTLINED,
        tooltip="Mostrar/ocultar contraseña"
    )

    def toggle_password(e):
        pwd_input.password = not pwd_input.password
        eye_btn.icon = (
            ft.icons.REMOVE_RED_EYE if pwd_input.password else ft.icons.VISIBILITY_OFF
        )
        page.update()

    eye_btn.on_click = toggle_password

    def check_password(e=None):
        pwd = pwd_input.value or ""
        results.controls.clear()

        rules = [
            ("Mínimo 8 caracteres", len(pwd) >= 8),
            ("Al menos 1 mayúscula", bool(re.search(r"[A-Z]", pwd))),
            ("Al menos 1 minúscula", bool(re.search(r"[a-z]", pwd))),
            ("Al menos 2 números", len(re.findall(r"\d", pwd)) >= 2),
            ("Al menos 1 carácter especial", bool(re.search(r"[!@#\$%\^&\*]", pwd))),
        ]
        custom = [
            ("Incluye '<3'", '<3' in pwd),
            ("Contiene emoji '😎'", '😎' in pwd),
        ]

        all_ok = True
        for desc, ok in rules + custom:
            all_ok &= ok
            icon = ft.icons.CHECK_CIRCLE if ok else ft.icons.CANCEL
            color = ft.colors.GREEN if ok else ft.colors.RED
            results.controls.append(
                ft.Row([ft.Icon(icon, color=color), ft.Text(desc)])
            )

        final = "✅ ¡Contraseña aceptada!" if all_ok else "❌ Intenta de nuevo"
        results.controls.append(ft.Divider())
        results.controls.append(ft.Text(final, weight=ft.FontWeight.BOLD))

        if all_ok:
            page.snack_bar = ft.SnackBar(
                ft.Text("🎉 Perfecto! Tu contraseña es segura para guardar tus secretos.")
            )
            page.snack_bar.open = True

        page.update()

    pwd_input.on_change = check_password

    rules_dlg = ft.AlertDialog(
        title=ft.Text("📜 Reglas personalizadas"),
        content=ft.Column([
            ft.Text("1. La suma de todos los dígitos debe ser 21."),
            ft.Text("2. Debe contener al menos un emoji '😎'."),
        ], spacing=5),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: setattr(rules_dlg, 'open', False))
        ],
        modal=True
    )

    title_row = ft.Row([
        ft.Text(
            "🔒 Password Checker", 
            size=24, 
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        ),
        ft.IconButton(
            icon=ft.icons.INFO_OUTLINE,
            tooltip="Ver reglas personalizadas",
            on_click=lambda e: setattr(rules_dlg, 'open', True)
        )
    ], alignment=ft.MainAxisAlignment.CENTER)


    results_label = ft.Text("Resultados:", size=16, weight=ft.FontWeight.BOLD)

    page.add(
        title_row,
        ft.Row([pwd_input, eye_btn], alignment=ft.MainAxisAlignment.CENTER),
        results_label,
        results,
        rules_dlg
    )

ft.app(target=main)
