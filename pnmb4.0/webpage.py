def webpage_html(additional_info: str = "") -> str:
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>PNMB4 Control</title>
            </head>
            <center><b>
            <form action="./forward">
            <input type="submit" value="Vorw&auml;rts" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Links" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./stop">
            <input type="submit" value="Stop" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Rechts" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            <form action="./back">
            <input type="submit" value="R&uuml;ckw&auml;rts" style="height:120px; width:120px" />
            </form>
            <p>{additional_info}</p>
            </body>
            </html>
            """
    return str(html)
