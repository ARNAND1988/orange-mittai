import { ref, computed } from "vue"
import api from "./api"

const tags = ref([])

const ALLOWED_TYPES = ["PROMOTION", "LABEL"]

export function useTagMenu() {
  const fetchTags = async () => {
    const res = await api.get("/tags")

    // res IS already the array
    tags.value = Array.isArray(res)
      ? res.filter(tag =>
          tag.is_active === true &&
          ALLOWED_TYPES.includes(tag.type)
        )
      : []
  }

  const groupedTags = computed(() => {
    return tags.value.reduce((acc, tag) => {
      if (!acc[tag.type]) acc[tag.type] = []
      acc[tag.type].push(tag)
      return acc
    }, {})
  })

  return {
    groupedTags,
    fetchTags
  }
}
