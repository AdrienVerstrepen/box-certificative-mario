export const sanitizeEmail = (email) => {
    const trimmedEmail = email.trim().toLowerCase()
    const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    if (!emailRegex.test(trimmedEmail)) {
        throw new Error("Invalid E-mail")
    }
    return trimmedEmail
}

export const sanitizeUsername = (username) => {
    const trimmedUsername = username.trim().toLowerCase()
    return trimmedUsername
}