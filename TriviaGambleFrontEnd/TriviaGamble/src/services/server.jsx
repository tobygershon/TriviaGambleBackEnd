import axios from 'axios'

const ourServer = axios.create({
    baseURL: 'http://127.0.0.1:5000/'
})

export async function getAnswer(answer) {
    const resp = await ourServer.get(answer)
    setTimeout(1000)
    return resp
}