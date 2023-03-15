from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer

class InvoiceTests(APITestCase):
    def test_create_invoice_with_invoice_details(self):
        url = reverse('invoice-list')
        data = {
            "date": "2023-03-15",
            "invoice_no": "INV001",
            "customer_name": "John Doe",
            "details": [
                {
                    "description": "Product A",
                    "quantity": 2,
                    "unit_price": 10.50,
                    "price": 21.00
                },
                {
                    "description": "Product B",
                    "quantity": 1,
                    "unit_price": 15.00,
                    "price": 15.00
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        print(response.data)  # print the response data to see what's causing the error
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        invoice = Invoice.objects.get(invoice_no='INV001')
        self.assertEqual(invoice.customer_name, 'John Doe')
        self.assertEqual(invoice.details.count(), 2)

    def test_get_all_invoices(self):
        url = reverse('invoice-list')
        response = self.client.get(url)
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


