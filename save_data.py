import datetime


def save_market_report(data_df):
    html_content = f"""
    <html>
    <head>
        <title>Market Update {datetime.date.today()}</title>
        <style>
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ padding: 8px; text-align: left; border: 1px solid #ddd; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>Market Update {datetime.date.today()}</h2>
        {data_df.to_html()}
        <p>Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </body>
    </html>
    """

    with open('market_report.html', 'w') as f:
        f.write(html_content)
