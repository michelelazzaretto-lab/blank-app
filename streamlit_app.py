import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

    
import streamlit as st


LOGO_URL = "https://myholiday.krossbooking.com/images/21/logo-sidebar-desktop.png?cdn=0"

PREDEFINED_RECIPIENT = "michele.lazzaretto@gmail.com"

PERIOD_PRIORITY = {
    "promozionale": 0,
    "stagione": 1,
    "alta stagione": 2,
}

PERIOD_PRICE_TIERS = {
    "alta stagione": {
        1: {"adult": 74.50, "junior": 37.00, "youth": 63.00, "senior": 63.00},
        2: {"adult": 143.50, "junior": 71.50, "youth": 121.50, "senior": 121.50},
        3: {"adult": 212.00, "junior": 106.00, "youth": 180.50, "senior": 180.50},
        4: {"adult": 278.50, "junior": 139.00, "youth": 236.50, "senior": 236.50},
        5: {"adult": 343.00, "junior": 171.50, "youth": 292.00, "senior": 292.00},
        6: {"adult": 374.50, "junior": 187.00, "youth": 318.50, "senior": 318.50},
        7: {"adult": 406.50, "junior": 203.00, "youth": 345.50, "senior": 345.50},
        8: {"adult": 437.00, "junior": 218.50, "youth": 371.50, "senior": 371.50},
        9: {"adult": 465.50, "junior": 232.50, "youth": 396.00, "senior": 396.00},
        10: {"adult": 493.00, "junior": 246.50, "youth": 419.00, "senior": 419.00},
        11: {"adult": 521.00, "junior": 260.50, "youth": 443.00, "senior": 443.00},
        12: {"adult": 549.00, "junior": 274.50, "youth": 466.50, "senior": 466.50},
        13: {"adult": 577.00, "junior": 288.50, "youth": 490.50, "senior": 490.50},
        14: {"adult": 602.00, "junior": 301.00, "youth": 512.00, "senior": 512.00},
    },
    "stagione": {
        1: {"adult": 66.00, "junior": 33.00, "youth": 56.50, "senior": 56.50},
        2: {"adult": 127.00, "junior": 63.50, "youth": 108.00, "senior": 108.00},
        3: {"adult": 188.00, "junior": 94.00, "youth": 160.00, "senior": 160.00},
        4: {"adult": 246.00, "junior": 123.00, "youth": 209.00, "senior": 209.00},
        5: {"adult": 303.50, "junior": 151.50, "youth": 258.00, "senior": 258.00},
        6: {"adult": 331.00, "junior": 165.50, "youth": 281.00, "senior": 281.00},
        7: {"adult": 358.50, "junior": 179.00, "youth": 304.50, "senior": 304.50},
        8: {"adult": 387.00, "junior": 193.50, "youth": 329.00, "senior": 329.00},
        9: {"adult": 411.00, "junior": 205.50, "youth": 349.50, "senior": 349.50},
        10: {"adult": 435.50, "junior": 217.00, "youth": 370.00, "senior": 370.00},
        11: {"adult": 460.50, "junior": 230.00, "youth": 391.50, "senior": 391.50},
        12: {"adult": 484.00, "junior": 242.00, "youth": 411.00, "senior": 411.00},
        13: {"adult": 508.00, "junior": 254.00, "youth": 432.00, "senior": 432.00},
        14: {"adult": 531.00, "junior": 265.50, "youth": 451.00, "senior": 451.00},
    },
    "promozionale": {
        1: {"adult": 51.50, "junior": 25.50, "youth": 44.00, "senior": 44.00},
        2: {"adult": 99.00, "junior": 49.50, "youth": 84.00, "senior": 84.00},
        3: {"adult": 147.00, "junior": 73.50, "youth": 124.50, "senior": 124.50},
        4: {"adult": 192.00, "junior": 96.50, "youth": 163.50, "senior": 163.50},
        5: {"adult": 237.00, "junior": 118.50, "youth": 201.50, "senior": 201.50},
        6: {"adult": 258.50, "junior": 129.50, "youth": 220.00, "senior": 220.00},
        7: {"adult": 279.50, "junior": 140.00, "youth": 238.00, "senior": 238.00},
        8: {"adult": 302.00, "junior": 151.00, "youth": 256.50, "senior": 256.50},
        9: {"adult": 321.00, "junior": 160.50, "youth": 273.00, "senior": 273.00},
        10: {"adult": 340.00, "junior": 170.00, "youth": 289.00, "senior": 289.00},
        11: {"adult": 359.00, "junior": 179.50, "youth": 305.00, "senior": 305.00},
        12: {"adult": 377.50, "junior": 189.00, "youth": 321.00, "senior": 321.00},
        13: {"adult": 396.50, "junior": 198.00, "youth": 337.50, "senior": 337.50},
        14: {"adult": 414.00, "junior": 207.00, "youth": 351.50, "senior": 351.50},
    },
}

PERIODS = {
    "alta stagione": [
        ("2026-12-26", "2027-01-08"),
        ("2027-01-30", "2027-03-29"),
    ],
    "stagione": [
        ("2026-12-19", "2026-12-25"),
        ("2027-01-09", "2027-01-29"),
        ("2027-03-30", "2027-04-09"),
    ],
    "promozionale": [
        ("2026-11-28", "2026-12-18"),
        ("2027-04-10", "2027-05-02"),
    ],
}


def in_periods(date_to_check, periods):
    for start_str, end_str in periods:
        start = datetime.fromisoformat(start_str).date()
        end = datetime.fromisoformat(end_str).date()
        if start <= date_to_check <= end:
            return True
    return False


PERIOD_DAILY_PRICES = {
    "alta stagione": {"adult": 74.50, "junior": 37.00, "youth": 63.00, "senior": 63.00, "baby": 0.0},
    "stagione": {"adult": 66.00, "junior": 33.00, "youth": 56.50, "senior": 56.50, "baby": 0.0},
    "promozionale": {"adult": 51.50, "junior": 25.50, "youth": 44.00, "senior": 44.00, "baby": 0.0},
}


def get_skipass_period_for_date(current_date):
    for period_name, period_ranges in PERIODS.items():
        if in_periods(current_date, period_ranges):
            return period_name
    return None


def get_period_info_for_date(current_date):
    for period_name, period_ranges in PERIODS.items():
        for start_str, end_str in period_ranges:
            start = datetime.fromisoformat(start_str).date()
            end = datetime.fromisoformat(end_str).date()
            if start <= current_date <= end:
                return period_name, start, end
    return None


def should_show_days_warning(num_days, max_days):
    return max_days < 14 and num_days > max_days


def get_num_giorni_bounds(start_date):
    period_info = get_period_info_for_date(start_date)
    if period_info is None:
        return 5, 5, 5

    min_days = 5
    max_days = 14
    default_days = 5
    return min_days, max_days, default_days


def get_contiguous_end_date(start_date):
    valid_ranges = sorted(
        (
            datetime.fromisoformat(start_str).date(),
            datetime.fromisoformat(end_str).date(),
        )
        for period_ranges in PERIODS.values()
        for start_str, end_str in period_ranges
    )

    for start, end in valid_ranges:
        if start <= start_date <= end:
            return end
    return None


def is_reservation_valid(start_date, num_days):
    """Check if all days of the reservation are within valid periods."""
    for offset in range(num_days):
        current_date = start_date + timedelta(days=offset)
        if get_skipass_period_for_date(current_date) is None:
            return False
    return True


def choose_skipass_period(start_date, num_days):
    counts = {period_name: 0 for period_name in PERIODS}
    for offset in range(num_days):
        current_date = start_date + timedelta(days=offset)
        period_name = get_skipass_period_for_date(current_date)
        if period_name is None:
            continue
        counts[period_name] += 1

    best_period = None
    best_key = None
    for period_name, count in counts.items():
        if count == 0:
            continue
        season_price = PERIOD_PRICE_TIERS[period_name][num_days]["adult"]
        period_key = (count, season_price)
        if best_key is None or period_key > best_key:
            best_key = period_key
            best_period = period_name

    return best_period


def calculate_total_price(start_date, num_days, num_adulti, num_ridotti, num_young, num_senior, num_baby):
    daily_details = []
    category_totals = {
        "adult": 0.0,
        "junior": 0.0,
        "youth": 0.0,
        "senior": 0.0,
        "baby": 0.0,
    }
    segment_summary = []
    total_skiers = num_adulti + num_ridotti + num_young + num_senior + num_baby
    deposit_total = total_skiers * 5.0

    reservation_period = choose_skipass_period(start_date, num_days)

    for offset in range(num_days):
        current_date = start_date + timedelta(days=offset)
        period_name = get_skipass_period_for_date(current_date)
        if period_name is None:
            raise ValueError("La data selezionata esce dai periodi di apertura skipass.")

        prices = PERIOD_DAILY_PRICES[period_name]
        daily_details.append(
            {
                "data": current_date.isoformat(),
                "stagione": period_name,
                "adulto": prices["adult"],
                "junior": prices["junior"],
                "youth": prices["youth"],
                "senior": prices["senior"],
                "baby": prices.get("baby", 0.0),
                "totale_giornaliero": (
                    num_adulti * prices["adult"]
                    + num_ridotti * prices["junior"]
                    + num_young * prices["youth"]
                    + num_senior * prices["senior"]
                    + num_baby * prices.get("baby", 0.0)
                ),
            }
        )

    segment_prices = PERIOD_PRICE_TIERS[reservation_period][num_days]
    segment_total = (
        num_adulti * segment_prices["adult"]
        + num_ridotti * segment_prices["junior"]
        + num_young * segment_prices["youth"]
        + num_senior * segment_prices["senior"]
        + num_baby * segment_prices.get("baby", 0.0)
    )
    segment_summary.append(
        {
            "periodo": reservation_period,
            "durata": f"{num_days} giorni",
            "adulto": f"€ {segment_prices['adult']:.2f}",
            "junior": f"€ {segment_prices['junior']:.2f}",
            "youth": f"€ {segment_prices['youth']:.2f}",
            "senior": f"€ {segment_prices['senior']:.2f}",
            "baby": f"€ {segment_prices.get('baby', 0.0):.2f}",
            "totale_segmento": f"€ {segment_total:.2f}",
        }
    )
    category_totals["adult"] += num_adulti * segment_prices["adult"]
    category_totals["junior"] += num_ridotti * segment_prices["junior"]
    category_totals["youth"] += num_young * segment_prices["youth"]
    category_totals["senior"] += num_senior * segment_prices["senior"]
    category_totals["baby"] += num_baby * segment_prices.get("baby", 0.0)

    tariff_total = sum(category_totals.values())
    total = tariff_total + deposit_total

    pricing_summary = [
        {
            "Categoria": "adulto",
            "Numero selezionati": num_adulti,
            "Totale categoria": f"€ {category_totals['adult']:.2f}",
            "Prezzo medio/giorno": f"€ {category_totals['adult'] / num_days:.2f}",
        },
        {
            "Categoria": "junior",
            "Numero selezionati": num_ridotti,
            "Totale categoria": f"€ {category_totals['junior']:.2f}",
            "Prezzo medio/giorno": f"€ {category_totals['junior'] / num_days:.2f}",
        },
        {
            "Categoria": "youth",
            "Numero selezionati": num_young,
            "Totale categoria": f"€ {category_totals['youth']:.2f}",
            "Prezzo medio/giorno": f"€ {category_totals['youth'] / num_days:.2f}",
        },
        {
            "Categoria": "senior",
            "Numero selezionati": num_senior,
            "Totale categoria": f"€ {category_totals['senior']:.2f}",
            "Prezzo medio/giorno": f"€ {category_totals['senior'] / num_days:.2f}",
        },
        {
            "Categoria": "baby",
            "Numero selezionati": num_baby,
            "Totale categoria": f"€ {category_totals['baby']:.2f}",
            "Prezzo medio/giorno": f"€ {category_totals['baby'] / num_days:.2f}",
        },
        {
            "Categoria": "cauzione",
            "Numero selezionati": total_skiers,
            "Totale categoria": f"€ {deposit_total:.2f}",
            "Prezzo medio/giorno": f"€ {deposit_total / num_days:.2f}",
        },
    ]
    return total, reservation_period, pricing_summary, daily_details, segment_summary, tariff_total, deposit_total


def get_smtp_settings() -> dict[str, str]:
    default_settings = {
        "server": "",
        "port": "",
        "username": "",
        "password": "",
        "from_email": "",
    }

    env_values = {
        "server": os.getenv("SMTP_SERVER", "").strip(),
        "port": os.getenv("SMTP_PORT", "").strip(),
        "username": os.getenv("SMTP_USERNAME", "").strip(),
        "password": os.getenv("SMTP_PASSWORD", "").strip(),
        "from_email": os.getenv("SMTP_FROM_EMAIL", "").strip(),
    }
    if any(env_values.values()):
        return env_values

    try:
        secret_values = {
            "server": str(st.secrets.get("SMTP_SERVER", "")).strip(),
            "port": str(st.secrets.get("SMTP_PORT", "")).strip(),
            "username": str(st.secrets.get("SMTP_USERNAME", "")).strip(),
            "password": str(st.secrets.get("SMTP_PASSWORD", "")).strip(),
            "from_email": str(st.secrets.get("SMTP_FROM_EMAIL", "")).strip(),
        }
    except Exception:
        return default_settings

    return {
        key: value if value not in (None, "") else default_settings[key]
        for key, value in secret_values.items()
    }


def send_reservation_email(reservation: dict, total_price: int, customer_email: str, tariff_total: float, deposit_total: float, pricing_summary: list) -> tuple[bool, str]:
    smtp_settings = get_smtp_settings()
    smtp_server = smtp_settings["server"]
    smtp_port = smtp_settings["port"]
    smtp_username = smtp_settings["username"]
    smtp_password = smtp_settings["password"]
    smtp_from = smtp_settings["from_email"]

    if not all([smtp_server, smtp_port, smtp_username, smtp_password, smtp_from]):
        return False, (
            "Impossibile inviare email: mancanti le variabili d'ambiente SMTP_SERVER, "
            "SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD e SMTP_FROM_EMAIL."
        )

    recipients = [PREDEFINED_RECIPIENT, customer_email]
    subject = "Nuova prenotazione skipass"
    
    tariff_sconto_carta = tariff_total * 0.95
    tariff_sconto_contanti = tariff_total * 0.93
    total_card_with_deposit = tariff_sconto_carta + deposit_total
    total_cash_with_deposit = tariff_sconto_contanti + deposit_total

    body_lines = [
        "Customer / Cliente",
        f"Riferimento: {reservation['nome']}",
        "",
        "Dettaglio prenotazione skipass / Reservation details",
        f"Skipass valido dal / Valid from: {reservation['data_inizio']}",
        f"Numero di giorni / Number of days: {reservation['num_giorni']}",
        "",
        "Categorie / Categories",
    ]
    
    for row in pricing_summary:
        categoria = row["Categoria"]
        if categoria == "cauzione":
            continue
        num = row["Numero selezionati"]
        if num <= 0:
            continue
        importo = row["Totale categoria"]
        body_lines.append(f"  {categoria.capitalize()}: {num} x {importo}")
    
    body_lines.extend([
        "",
        "Riepilogo totali / Payment Summary",
        f"Tariffa totale / Total tariff: € {tariff_total:.2f}",
        f"Cauzione / Deposit: € {deposit_total:.2f}",
        f"Totale generale / Total: € {total_price:.2f}",
        "",
        "Opzioni di pagamento / Payment Options",
        f"Con carta (5% sconto) / Card (5% discount): € {tariff_sconto_carta:.2f} + cauzione € {deposit_total:.2f} = € {total_card_with_deposit:.2f}",
        f"In contanti (7% sconto) / Cash (7% discount): € {tariff_sconto_contanti:.2f} + cauzione € {deposit_total:.2f} = € {total_cash_with_deposit:.2f}",
        "",
        f"Email: {customer_email}",
    ])

    message = EmailMessage()
    message["From"] = smtp_from
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    html_body = f"""
    <html>
      <body>
        <img src="{LOGO_URL}" alt="Logo skipass" style="max-width: 280px; height: auto; margin-bottom: 16px;" />
        <pre style="font-family: Arial, sans-serif; white-space: pre-wrap;">{''.join(f'{line}\n' for line in body_lines)}</pre>
      </body>
    </html>
    """
    message.set_content("\n".join(body_lines))
    message.add_alternative(html_body, subtype="html")

    try:
        port_number = int(smtp_port)
    except ValueError:
        return False, "SMTP_PORT deve essere un numero intero valido."

    try:
        if port_number == 465:
            server = smtplib.SMTP_SSL(smtp_server, port_number, timeout=20)
        else:
            server = smtplib.SMTP(smtp_server, port_number, timeout=20)
            server.starttls()

        server.login(smtp_username, smtp_password)
        server.send_message(message)
        server.quit()
        return True, "Email inviata correttamente ai destinatari."
    except Exception as exc:
        return False, f"Errore durante l'invio dell'email: {exc}"


def main() -> None:
    st.set_page_config(page_title="Reserve your skipass", page_icon="🎿")
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f5f7fb 0%, #eef3fb 100%);
            color: #0f172a;
        }
        div.block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1100px;
        }
        section[data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(26, 55, 101, 0.10);
            border-radius: 18px;
            padding: 1.4rem 1.2rem 1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
            color: #0f172a;
        }
        .reservation-card {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(26, 55, 101, 0.08);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            margin-top: 1rem;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
            color: #0f172a;
        }
        .summary-box {
            background: linear-gradient(180deg, #f8fbff 0%, #edf5ff 100%);
            border: 1px solid rgba(20, 119, 214, 0.16);
            border-radius: 14px;
            padding: 0.9rem 1rem;
            height: 100%;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
        }
        .summary-label {
            font-size: 0.72rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #4b5d7a;
            margin-bottom: 0.35rem;
            font-weight: 700;
        }
        .summary-value {
            font-size: 1.25rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.2;
        }
        .summary-section-title {
            margin: 0.6rem 0 0.7rem 0;
            font-size: 1rem;
            font-weight: 700;
            color: #0f172a;
        }
        .payment-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.8rem;
            font-size: 0.94rem;
        }
        .payment-table th, .payment-table td {
            padding: 0.8rem 0.7rem;
            text-align: left;
            border-bottom: 1px solid rgba(15, 23, 42, 0.08);
            vertical-align: top;
        }
        .payment-row-card {
            background: rgba(59, 130, 246, 0.08);
        }
        .payment-row-cash {
            background: rgba(16, 185, 129, 0.08);
        }
        .payment-tag {
            display: inline-block;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            padding: 0.22rem 0.5rem;
            border-radius: 999px;
            margin-bottom: 0.35rem;
        }
        .payment-tag-card {
            background: rgba(59, 130, 246, 0.14);
            color: #1d4ed8;
        }
        .payment-tag-cash {
            background: rgba(16, 185, 129, 0.14);
            color: #047857;
        }
        .section-label {
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #4b5d7a;
            margin: 0.7rem 0 0.5rem;
        }
        div[data-testid="stTextInput"] label,
        div[data-testid="stDateInput"] label,
        div[data-testid="stNumberInput"] label,
        div[data-testid="stTextInput"] p,
        div[data-testid="stDateInput"] p,
        div[data-testid="stNumberInput"] p {
            color: #0f172a !important;
            font-weight: 600 !important;
        }
        div[data-testid="stTable"] table,
        div[data-testid="stTable"] th,
        div[data-testid="stTable"] td {
            color: #0f172a !important;
            background-color: transparent !important;
        }
        div[data-testid="stDateInput"],
        div[data-testid="stNumberInput"] {
            width: 100% !important;
        }
        div[data-testid="stDateInput"] > div,
        div[data-testid="stNumberInput"] > div {
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
        div[data-testid="stDateInput"] label,
        div[data-testid="stNumberInput"] label {
            white-space: pre-line !important;
            display: block !important;
            line-height: 1.2 !important;
            text-align: left !important;
            min-height: 2.6em !important;
            margin-bottom: 0.35rem !important;
        }
        div[data-testid="stButton"] > button {
            border-radius: 10px;
            font-weight: 700;
            padding: 0.7rem 1.25rem;
            background: linear-gradient(180deg, #1f8fff 0%, #1477d6 100%);
            color: white;
            border: none;
        }
        div[data-testid="stButton"] > button:hover {
            filter: brightness(1.03);
        }

        @media (max-width: 768px) {
            div.block-container {
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }
            section[data-testid="stForm"] {
                padding: 1rem 0.8rem 0.8rem;
            }
            div[data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                max-width: 100% !important;
                flex: 0 0 100% !important;
            }
            div[data-testid="stButton"] > button {
                width: 100% !important;
            }
        }

        @media (prefers-color-scheme: light) {
            .stApp {
                background: linear-gradient(180deg, #f5f7fb 0%, #eef3fb 100%);
                color: #0f172a;
            }
            section[data-testid="stForm"],
            .reservation-card {
                background: rgba(255, 255, 255, 0.95);
                border-color: rgba(26, 55, 101, 0.12);
                color: #0f172a;
            }
            .summary-box {
                background: linear-gradient(180deg, #d4e6ff 0%, #bfd6ff 100%) !important;
                border: 2px solid rgba(29, 78, 216, 0.35) !important;
                box-shadow: inset 0 2px 4px rgba(29, 78, 216, 0.1) !important;
            }
            .section-label,
            .summary-label {
                color: #1f4a9f !important;
                font-weight: 900 !important;
                font-size: 0.75rem !important;
            }
            .summary-value {
                color: #0a1428 !important;
                font-weight: 900 !important;
                font-size: 1.35rem !important;
            }
            .summary-section-title {
                color: #0a1428 !important;
                font-weight: 900 !important;
                font-size: 1.1rem !important;
            }
            .payment-table th,
            .payment-table td {
                color: #1a2942 !important;
                border-bottom: 1px solid rgba(15, 23, 42, 0.12);
            }
            .payment-tag-card {
                background: rgba(59, 130, 246, 0.16);
                color: #1d4ed8;
            }
            .payment-tag-cash {
                background: rgba(16, 185, 129, 0.16);
                color: #047857;
            }
            div[data-testid="stButton"] > button {
                background: linear-gradient(180deg, #1f8fff 0%, #1477d6 100%);
                color: #ffffff;
            }
            div[data-testid="stTextInput"] label,
            div[data-testid="stDateInput"] label,
            div[data-testid="stNumberInput"] label,
            div[data-testid="stTextInput"] p,
            div[data-testid="stDateInput"] p,
            div[data-testid="stNumberInput"] p {
                color: #1e3a5f !important;
            }
            div[data-testid="stTable"] table,
            div[data-testid="stTable"] th,
            div[data-testid="stTable"] td {
                color: #0a1428 !important;
            }
            [data-testid="metric-container"] {
                background: linear-gradient(180deg, #d4e6ff 0%, #bfd6ff 100%) !important;
                border: 2px solid rgba(29, 78, 216, 0.35) !important;
                border-radius: 14px !important;
                padding: 1rem !important;
            }
            [data-testid="metric-container"] > div {
                color: #0a1428 !important;
                font-weight: 900 !important;
            }
        }

        @media (prefers-color-scheme: dark) {
            .stApp {
                background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
                color: #edf3ff;
            }
            section[data-testid="stForm"],
            .reservation-card {
                background: rgba(15, 23, 42, 0.92);
                border-color: rgba(148, 163, 184, 0.2);
                color: #edf3ff;
                box-shadow: 0 10px 28px rgba(2, 6, 23, 0.45);
            }
            .section-label,
            .summary-label {
                color: #cbd5e1;
                font-weight: 700;
            }
            .summary-value {
                color: #f1f5f9;
            }
            .summary-section-title {
                color: #e2e8f0;
            }
            .payment-table th,
            .payment-table td {
                color: #cbd5e1;
                border-bottom: 1px solid rgba(148, 163, 184, 0.15);
            }
            .payment-tag-card {
                background: rgba(59, 130, 246, 0.2);
                color: #60a5fa;
            }
            .payment-tag-cash {
                background: rgba(16, 185, 129, 0.2);
                color: #34d399;
            }
            div[data-testid="stButton"] > button {
                background: linear-gradient(180deg, #2b7fff 0%, #1d5fd6 100%);
                color: #ffffff;
            }
            div[data-testid="stTextInput"] label,
            div[data-testid="stDateInput"] label,
            div[data-testid="stNumberInput"] label,
            div[data-testid="stTextInput"] p,
            div[data-testid="stDateInput"] p,
            div[data-testid="stNumberInput"] p {
                color: #e2e8f0 !important;
            }
            div[data-testid="stTable"] table,
            div[data-testid="stTable"] th,
            div[data-testid="stTable"] td {
                color: #f8fafc !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.columns(3)[1].image(LOGO_URL, width=340)
    st.title("Reserve your skipass")
    st.write(
        "Complete the form below and the total will be displayed after calculation. "
        "_Compila il modulo qui sotto e il totale verrà mostrato dopo il calcolo_."
    )

    if "reservation" not in st.session_state:
        st.session_state.reservation = None
        st.session_state.total_price = None
        st.session_state.tariff_total = None
        st.session_state.deposit_total = None
        st.session_state.selected_period = None
        st.session_state.pricing_summary = None
        st.session_state.daily_details = None
        st.session_state.segment_summary = None

    with st.form("reservation_form"):
        col_input_1, col_input_2 = st.columns([1.3, 1])
        with col_input_1:
            reservation_reference = st.text_input("Full name / reservation number _Nome e cognome / numero di prenotazione_")
        with col_input_2:
            email = st.text_input("Email address _Indirizzo email_")

        col_date_1, col_date_2 = st.columns([1.1, 1.1])
        with col_date_1:
            st.markdown("<div style='height: 100%;'>", unsafe_allow_html=True)
            data_inizio = st.date_input("Valid from _Valido dal_")
            st.session_state.data_inizio = data_inizio
            st.markdown("</div>", unsafe_allow_html=True)
        with col_date_2:
            min_days, max_days, default_days = get_num_giorni_bounds(data_inizio)
            st.markdown("<div style='height: 100%;'>", unsafe_allow_html=True)
            num_giorni = st.number_input(
                "Number of days _Numero di giorni_",
                min_value=5,
                max_value=14,
                value=6,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-label">Guest categories</div>', unsafe_allow_html=True)
        category_cols = st.columns([1.05, 1.35, 1.35, 1.35, 1.35])
        with category_cols[0]:
            num_adulti = st.number_input("Adults\n_Adulti_", min_value=0, max_value=20, value=1)
        with category_cols[1]:
            num_ridotti = st.number_input("Junior (born 2011-2018)\n_Junior (nati dal 2011 al 2018)_", min_value=0, max_value=20, value=0)
        with category_cols[2]:
            num_young = st.number_input("Youth (born 2002-2010)\n_Youth (nati dal 2002 al 2010)_", min_value=0, max_value=20, value=0)
        with category_cols[3]:
            num_senior = st.number_input("Senior (born before 2002)\n_Senior (nati prima del 2002)_", min_value=0, max_value=20, value=0)
        with category_cols[4]:
            num_baby = st.number_input("Baby (born from 2019 onwards)\n_Baby (nati dal 2019 in avanti)_", min_value=0, max_value=20, value=0)

        submit_calc = st.form_submit_button("Calculate _Calcola_", use_container_width=True)

    if submit_calc:
        if get_period_info_for_date(data_inizio) is None:
            st.error(
                "Invalid start date. Please select a date within the winter opening periods. "
                "Valid periods run from 28/11/2026 to 02/05/2027. "
                "_Data iniziale non valida. Seleziona una data all'interno dei periodi di apertura invernali. "
                "I periodi validi vanno dal 28/11/2026 al 02/05/2027._"
            )
        elif not is_reservation_valid(data_inizio, num_giorni):
            st.error(
                f"Invalid reservation: the selected {num_giorni} days extend beyond the valid ski periods. "
                "Please choose a different start date or number of days. "
                f"_Prenotazione non valida: i {num_giorni} giorni selezionati vanno oltre i periodi di validità degli impianti. "
                "Seleziona una data diversa o un numero di giorni diverso._"
            )
        elif not reservation_reference.strip():
            st.error("Please enter your full name or reservation number. _Inserisci nome e cognome oppure il numero di prenotazione._")
        elif not email.strip() or "@" not in email:
            st.error("Please enter a valid email address. _Inserisci un indirizzo email valido._")
        elif num_adulti + num_ridotti + num_young + num_senior + num_baby == 0:
            st.error("Please select at least one person. _Seleziona almeno una persona._")
        else:
            total_price, selected_period, pricing_summary, daily_details, segment_summary, tariff_total, deposit_total = calculate_total_price(
                data_inizio,
                num_giorni,
                num_adulti,
                num_ridotti,
                num_young,
                num_senior,
                num_baby,
            )
            st.session_state.reservation = {
                "nome": reservation_reference.strip(),
                "cognome": "",
                "data_inizio": data_inizio.isoformat(),
                "num_giorni": num_giorni,
                "num_adulti": num_adulti,
                "num_ridotti": num_ridotti,
                "num_young": num_young,
                "num_senior": num_senior,
                "num_baby": num_baby,
                "periodo_applicato": selected_period,
                "email": email.strip(),
            }
            st.session_state.total_price = total_price
            st.session_state.tariff_total = tariff_total
            st.session_state.deposit_total = deposit_total
            st.session_state.selected_period = selected_period
            st.session_state.pricing_summary = pricing_summary
            st.session_state.daily_details = daily_details
            st.session_state.segment_summary = segment_summary

            if should_show_days_warning(num_giorni, max_days):
                st.warning(
                    f"The maximum number of valid days for this date is {max_days}, "
                    "to avoid exceeding the ski area opening period. "
                    f"_Il numero massimo di giorni validi per questa data è {max_days}, "
                    "per non superare il periodo di apertura degli impianti._"
                )

    if st.session_state.reservation is not None:
        table_rows = []
        for row in st.session_state.pricing_summary:
            if row["Categoria"] == "cauzione":
                continue
            quantity = row["Numero selezionati"]
            if quantity <= 0:
                continue
            table_rows.append(
                {
                    "Validity from _Validità dal_": st.session_state.reservation["data_inizio"],
                    "Category _Categoria_": row["Categoria"].title(),
                    "Quantity _Quantità_": quantity,
                    "Amount _Importo_": row["Totale categoria"],
                    "Number of days _Numero di giorni_": st.session_state.reservation["num_giorni"],
                }
            )

        if table_rows:
            st.markdown('<div class="reservation-card">', unsafe_allow_html=True)
            st.table(table_rows)
            st.markdown('</div>', unsafe_allow_html=True)

        tariff_sconto_carta = st.session_state.tariff_total * 0.95
        tariff_sconto_contanti = st.session_state.tariff_total * 0.93
        total_card_with_deposit = tariff_sconto_carta + st.session_state.deposit_total
        total_cash_with_deposit = tariff_sconto_contanti + st.session_state.deposit_total

        st.markdown('<div class="reservation-card">', unsafe_allow_html=True)
        summary_cols = st.columns(2)

        with summary_cols[0]:
            st.markdown('<div class="summary-section-title">Total / Totale</div>', unsafe_allow_html=True)
            total_value = f"€ {st.session_state.total_price:.2f}"
            st.metric(
                label="Total Amount",
                value=total_value,
                label_visibility="collapsed"
            )

        with summary_cols[1]:
            st.markdown('<div class="summary-section-title">Deposit / Cauzione</div>', unsafe_allow_html=True)
            deposit_value = f"€ {st.session_state.deposit_total:.2f}"
            st.metric(
                label="Deposit Amount",
                value=deposit_value,
                label_visibility="collapsed"
            )

        st.markdown(
            f"""
            <table class="payment-table">
              <thead>
                <tr>
                  <th>Payment option / Opzione di pagamento</th>
                  <th>Discounted tariff / Tariffa scontata</th>
                  <th>Total with deposit / Totale con cauzione</th>
                </tr>
              </thead>
              <tbody>
                <tr class="payment-row-card">
                  <td>
                    <span class="payment-tag payment-tag-card">Card / Carta</span><br>
                    Card Payment / Pagamento con carta<br>
                    <strong>(5% discount / 5% sconto)</strong>
                  </td>
                  <td>€ {tariff_sconto_carta:.2f}</td>
                  <td><strong>€ {total_card_with_deposit:.2f}</strong></td>
                </tr>
                <tr class="payment-row-cash">
                  <td>
                    <span class="payment-tag payment-tag-cash">Cash / Contanti</span><br>
                    Cash payment / Pagamento in contanti<br>
                    <strong>(7% discount / 7% sconto)</strong>
                  </td>
                  <td>€ {tariff_sconto_contanti:.2f}</td>
                  <td><strong>€ {total_cash_with_deposit:.2f}</strong></td>
                </tr>
              </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Send _Invia_", use_container_width=True):
            sent, message = send_reservation_email(
                st.session_state.reservation,
                st.session_state.total_price,
                st.session_state.reservation["email"],
                st.session_state.tariff_total,
                st.session_state.deposit_total,
                st.session_state.pricing_summary,
            )
            if sent:
                st.success(message)
            else:
                st.error(message)


if __name__ == "__main__":
    main()









