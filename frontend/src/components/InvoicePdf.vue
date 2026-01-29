<script setup>
import { defineProps, defineExpose } from "vue"
import { LOGO_BASE64 } from "@/utils/logoBase64"

const props = defineProps({
  order: {
    type: Object,
    required: true,
  },
})

const generate = async () => {
  const pdfMakeModule = await import("pdfmake/build/pdfmake")
  const pdfFonts = await import("pdfmake/build/vfs_fonts")

  const pdfMake =
    pdfMakeModule.default ?? pdfMakeModule

  pdfMake.vfs = pdfFonts.default.vfs
  const order = props.order ?? {}

  // SAFELY extract fields
  const orderId = order.order_id ?? "N/A"
  const createdAt = order.created_at
    ? new Date(order.created_at).toLocaleString()
    : "N/A"
  const status = typeof order.status === "string"
    ? order.status.replaceAll("_", " ")
    : "N/A"

  // SAFELY extract items
  const items = Array.isArray(order.items)
    ? order.items
    : []

  if (!items.length) {
    console.warn("InvoicePdf: order has no items", order)
  }

  const itemsTable = [
    [
      { text: "Product", bold: true },
      { text: "Qty", bold: true },
      { text: "Price", bold: true, alignment: "right" },
    ],
    ...items.map((item) => [
      item.product_name ?? "Item",
      item.quantity ?? 1,
      {
        text: `€${((item.price ?? 0) * (item.quantity ?? 1)).toFixed(2)}`,
        alignment: "right",
      },
    ]),
  ]

  const totalAmount = order.total_amount ?? 0

  const docDefinition = {
    pageSize: "A4",
    pageMargins: [40, 40, 40, 40],
    watermark: {
      text: status,
      color: 'gray',
      opacity: 0.2,
      bold: true,
      fontSize: 60,
      angle: -45
    },
    content: [
      /* HEADER */
      {
        columns: [
          {
            image: LOGO_BASE64,
            width: 80,
          },
          {
            stack: [
              { text: "Orange Mittai", bold: true },
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

      /* ORDER INFO */
      {
        columns: [
          {
            stack: [
              { text: "Order ID:", bold: true },
              orderId,
              { text: "Date:", bold: true, margin: [0, 8, 0, 0] },
              createdAt,
              { text: "Status:", bold: true, margin: [0, 8, 0, 0] },
              status,
            ],
          },
        ],
        margin: [0, 20, 0, 20],
      },

      /* ITEMS */
      {
        table: {
          widths: ["*", 50, 80],
          body: itemsTable,
        },
        layout: {
          fillColor: (rowIndex) =>
            rowIndex === 0 ? "#eeeeee" : null,
        },
      },

      /* TOTAL */
      {
        columns: [
          { width: "*", text: "" },
          {
            width: 250,
            table: {
              widths: ["*", "auto"],
              body: [
                [
                  { text: "Total", bold: true },
                  { text: `€${totalAmount.toFixed(2)}`, bold: true },
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
      title: {
        fontSize: 22,
        bold: true,
        margin: [0, 30, 0, 20],
      },
    },
  }

  pdfMake.createPdf(docDefinition).download(
    `invoice-${orderId}.pdf`
  )
}

/* 👇 expose method to parent */
defineExpose({ generate })
</script>

<template>
  <!-- no UI needed -->
  <div />
</template>
