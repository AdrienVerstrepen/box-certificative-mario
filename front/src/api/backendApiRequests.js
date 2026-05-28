import backendClientConf from '@/api/backendClientConf'

export const sendRegistrationRequest = async (username, mail, password) => {
    try {
        const response = await backendClientConf.get(`/?username=${username}&mail=${mail}&password=${password}`)
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

export const sendLoginRequest = async (mail, password) => {
    try {
        const response = await backendClientConf.get(`/?mail=${mail}&password=${password}`)
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