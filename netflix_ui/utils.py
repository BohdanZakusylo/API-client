import matplotlib.pyplot as plt
from io import BytesIO
import base64
import httpx

plt.switch_backend('Agg')

async def fetch_data_and_generate_pie_chart(api_url, token):
    async with httpx.AsyncClient() as client:
        # Make an asynchronous API call
        response_4 = await client.get(api_url + "4" + f"?token={token}")
        response_4.raise_for_status()
        response_5 = await client.get(api_url + "5" + f"?token={token}")
        response_5.raise_for_status()

        data_4 = response_4.json()
        data_5 = response_5.json()

        values = [data_4, data_5]
        labels = ['UA', 'EN']

        # Generate the pie chart
        chart_base64 = await generate_pie_chart(values, labels)

    return chart_base64

async def generate_pie_chart(values, labels):
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.axis("equal")

    chart_image = BytesIO()
    plt.savefig(chart_image, format="png")
    chart_image.seek(0)
    plt.close()

    chart_base64 = base64.b64encode(chart_image.read()).decode("utf-8")
    return chart_base64

