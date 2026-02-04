// src/services/SearchService.js
import { ref } from "vue"

export const searchQuery = ref("")

export function useSearch() {
  return {
    searchQuery
  }
}
