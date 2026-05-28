import { describe, it, expect, vi } from 'vitest'
import { getSearchResult } from '@/api/geocodingApiRequests'
import geocodingApiClient from '@/api/geocodingClientConf'

vi.mock('@/api/geocodingClientConf', () => {
  return {
    default: {
      get: vi.fn()
    }
  }
})

describe('@/api/getSearchResult', () => {
  it('Returns API call results when it succeeds', async () => {
    const mockData = [{ place_id: 1, display_name: 'Paris' }]
    geocodingApiClient.get.mockResolvedValue({ data: mockData })
    const result = await getSearchResult('Paris')
    expect(result).toEqual(mockData)
  })

  it('Handle server errors', async () => {
    const error = { response: { status: 404 } }
    geocodingApiClient.get.mockRejectedValue(error)
    
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {})
    
    await getSearchResult('Inconnu')
    
    expect(spy).toHaveBeenCalled()
    spy.mockRestore()
  })
})