/**
 * 数据加载工具
 */

let dataCache: Record<string, any> = {}

export async function loadData(name: string): Promise<any> {
  if (dataCache[name]) return dataCache[name]
  const resp = await fetch(`${import.meta.env.BASE_URL}data/${name}.json`)
  const data = await resp.json()
  dataCache[name] = data
  return data
}

export async function loadMetadata() {
  return loadData('metadata')
}

export async function loadPlaceSummary() {
  return loadData('place_summary') as Promise<Record<string, PlaceSummary>>
}

export async function loadPlaces() {
  return loadData('places') as Promise<Place[]>
}

export async function loadWorks() {
  return loadData('works') as Promise<Work[]>
}

export async function loadAuthors() {
  return loadData('authors') as Promise<Author[]>
}

export async function loadSearchIndex() {
  return loadData('search_index') as Promise<SearchItem[]>
}

export async function loadConclusions() {
  return loadData('conclusions') as Promise<Conclusion[]>
}

export async function loadMethodology() {
  return loadData('methodology')
}

export async function loadDynastyPlaceSummary() {
  return loadData('dynasty_place_summary')
}

export async function loadAnalysis() {
  return loadData('analysis')
}

export async function loadImagerySummary() {
  return loadData('imagery_summary')
}

export async function loadThemes() {
  return loadData('themes')
}

export async function loadPlaceMentions() {
  return loadData('place_mentions') as Promise<PlaceMention[]>
}

// 类型定义
export interface PlaceSummary {
  place_id: string
  place_name: string
  place_type: string
  modern_name: string
  modern_province: string
  longitude: number
  latitude: number
  mapping_level: string
  mention_count: number
  tang_count: number
  song_count: number
  authors: string[]
  work_ids: string[]
}

export interface Place {
  place_id: string
  place_name: string
  place_name_normalized: string
  place_type: string
  historical_name: string
  modern_name: string
  modern_province: string
  modern_city: string
  longitude: number
  latitude: number
  mapping_level: string
  mapping_confidence: number
  mapping_source: string
  aliases: string[]
}

export interface Work {
  work_id: string
  title: string
  author_id: string
  author_name: string
  dynasty: string
  genre: string
  text: string
  text_hash: string
  source_id: string
  place_mentions: string[]
  imagery: string[]
  themes: string[]
  season_imagery: string[]
  moods: string[]
  is_target_author: boolean
}

export interface Author {
  author_id: string
  author_name: string
  dynasty: string
  birth_year: number | null
  death_year: number | null
  birth_place_raw: string
  biography_summary: string
  source_id: string
}

export interface SearchItem {
  work_id: string
  title: string
  author: string
  dynasty: string
  text: string
  places: string[]
  themes: string[]
  imagery: string[]
}

export interface Conclusion {
  conclusion_id: string
  text: string
  metric: string
  value: any
  dataset_version: string
  generated_at: string
}

export interface PlaceMention {
  work_id: string
  place_name: string
  place_name_normalized: string
  place_type: string
  context: string
  modern_name: string
  modern_province: string
  longitude: number
  latitude: number
  mapping_level: string
  dynasty: string
  author_name: string
}
