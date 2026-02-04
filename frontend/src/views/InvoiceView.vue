<template>
  <button @click="generatePDF">
    Download Invoice
  </button>
</template>

<script setup>
const generatePDF = async () => {
  const pdfMake = (await import("pdfmake/build/pdfmake")).default
  const pdfFonts = await import("pdfmake/build/vfs_fonts")

  pdfMake.vfs = pdfFonts.default.vfs

  /* MOCK DATA (replace with real order data) */
  const order = {
    id: "OM-102",
    date: "12 Jan 2026",
    payment: "UPI",
  }

  const customer = {
    name: "John Doe",
    address: "Anna Nagar, Chennai",
  }

  const items = [
    { name: "Mango Mittai", qty: 3, price: 150 },
    { name: "Jaggery Laddu", qty: 2, price: 120 },
  ]

  const subtotal = items.reduce(
    (s, i) => s + i.qty * i.price,
    0
  )
  const shipping = 40
  const total = subtotal + shipping

  /* ITEMS TABLE BODY */
  const itemsTableBody = [
    [
      { text: "Product", style: "tableHeader" },
      { text: "Qty", style: "tableHeader" },
      { text: "Price", style: "tableHeader", alignment: "right" },
    ],
    ...items.map((item) => [
      item.name,
      item.qty,
      { text: `€${item.price * item.qty}`, alignment: "right" },
    ]),
  ]

  const docDefinition = {
    pageSize: "A4",
    pageMargins: [40, 40, 40, 40],

    content: [
      /* HEADER */
      {
        columns: [
          {
            text: "Orange Mittai",
            style: "company",
          },
          {
            stack: [
              "Chennai, India",
              "+91 98765 43210",
              "support@orangemittai.com",
            ],
            alignment: "right",
            fontSize: 10,
          },
        ],
      },

      { text: "INVOICE", style: "title" },

      /* INFO GRID */
      {
        columns: [
          {
            stack: [
              { text: "Bill To:", bold: true },
              customer.name,
              customer.address,
            ],
          },
          {
            stack: [
              { text: "Ship To:", bold: true },
              customer.name,
              customer.address,
            ],
          },
          {
            stack: [
              { text: "Invoice #:", bold: true },
              order.id,
              { text: "Date:", bold: true, margin: [0, 8, 0, 0] },
              order.date,
              { text: "Payment:", bold: true, margin: [0, 8, 0, 0] },
              order.payment,
            ],
          },
        ],
        columnGap: 20,
        margin: [0, 20, 0, 20],
      },

      /* ITEMS TABLE */
      {
        table: {
          widths: ["*", 60, 80],
          body: itemsTableBody,
        },
        layout: {
          fillColor: (rowIndex) =>
            rowIndex === 0 ? "#000000" : null,
          hLineColor: "#dddddd",
          vLineColor: "#dddddd",
        },
      },

      /* TOTALS */
      {
        columns: [
          { width: "*", text: "" },
          {
            width: 250,
            table: {
              widths: ["*", "auto"],
              body: [
                ["Subtotal", `€${subtotal}`],
                ["Shipping", `€${shipping}`],
                [
                  { text: "Total", bold: true },
                  { text: `€${total}`, bold: true },
                ],
              ],
            },
            layout: "noBorders",
            margin: [0, 20, 0, 0],
          },
        ],
      },
    ],

    styles: {
      company: {
        fontSize: 14,
        bold: true,
      },
      title: {
        fontSize: 24,
        bold: true,
        margin: [0, 30, 0, 20],
      },
      tableHeader: {
        color: "white",
        bold: true,
      },
    },
  }

  pdfMake.createPdf(docDefinition).download(
    `invoice-${order.id}.pdf`
  )
}
</script>
