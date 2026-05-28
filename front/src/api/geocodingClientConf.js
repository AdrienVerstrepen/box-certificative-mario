import axios from 'axios';

const geocodingApiClient = axios.create({
	baseURL : 'https://nominatim.openstreetmap.org',
	timeout: 5000,
	headers: { 'User-Agent': 'travel-planning-app' },
});

export default geocodingApiClient;