import datetime


def save_market_report(data_df, monday, friday):
    html_content = f"""
    <html>
    <head>
        <title>Market Update from {monday} to {friday}</title>
        <style>
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ padding: 8px; text-align: left; border: 1px solid #ddd; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>Market Update from {monday} to {friday}</h2>
        {data_df.to_html()}
        Stock names that have a '=' in the name refer to commodities, so Gold, Silver, Brent Oil, Wheat, and Copper.
        <p>Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </body>
    </html>
    """

    with open('market_report.html', 'w') as f:
        f.write(html_content)
