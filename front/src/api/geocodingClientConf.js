import axios from 'axios'

const geocodingApiClient = axios.create({
	baseURL : 'https://nominatim.openstreetmap.org',
	timeout: 5000,
	
})

export default geocodingApiClient
