import geocodingApiClient from "./geocodingClientConf"

export const getSearchResult = async (query) => {
    try {
        const response = await geocodingApiClient.get(`/search?q=${query}&format=jsonv2`)
        return response.data
    } catch (error) {
        console.warn(error)
        if (error.response) {
            
        } else if (error.request) {
            
        } else { 
            
        }
    }
}