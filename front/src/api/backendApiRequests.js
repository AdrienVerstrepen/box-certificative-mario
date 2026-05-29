import backendClientConf from '@/api/backendClientConf'

export const sendRegistrationRequest = async (username, mail, password) => {
    try {
        const response = await backendClientConf.post('/api/register', {
            name: username,
            email: mail,
            password,
        })
        return response.data
    } catch (error) {
        if (error.response) {
            console.error("The API encountered an error :", error)
            throw new Error(error.response.data?.error || "Registration failed")
        } else if (error.request) {
            console.error("No response from the API :", error)
            throw new Error("No response from the API")
        } else { 
            console.error("Uknown error :", error)
            throw new Error("Unknown registration error")
        }
    }
}

export const sendLoginRequest = async (mail, password) => {
    try {
        const response = await backendClientConf.post('/api/login', {
            email: mail,
            password,
        })
        return response.data
    } catch (error) {
        if (error.response) {
            console.error("The API encountered an error :", error)
            throw new Error(error.response.data?.error || "Login failed")
        } else if (error.request) {
            console.error("No response from the API :", error)
            throw new Error("No response from the API")
        } else { 
            console.error("Uknown error :", error)
            throw new Error("Unknown login error")
        }
    }
}

export const sendPlacesRequest = async (tourName, places) => {
    try {
        const response = await backendClientConf.post('/api/places', {tourName, places})
        return response.data
    } catch (error) {

    }
}

export const checkIfTourIsPublic = async (tourId) => {
    try {
        const response = await backendClientConf.get(`/api/tour/${tourId}`)
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
