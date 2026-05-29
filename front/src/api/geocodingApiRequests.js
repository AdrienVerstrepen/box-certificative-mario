import geocodingApiClient from "./geocodingClientConf"

export const getSearchResult = async (query) => {
    try {
        const response = await geocodingApiClient.get(`/search?q=${query}&format=jsonv2`)
        console.log("API response :", response.data)
        return response.data
    } catch (error) {
        console.warn(error)
        if (error.response) {
            console.error("The API encountered an error :", error)
        } else if (error.request) {
            console.error("No response from the API :", error)
        } else { 
            console.error("Uknown error :", error)
        }
    }
}