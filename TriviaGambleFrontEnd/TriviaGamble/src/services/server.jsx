import axios from 'axios'

const ourServer = axios.create({
    baseURL: 'http://127.0.0.1:5000/'
})

export async function getAnswer(answer) {
    const resp = await ourServer.get(answer)
    setTimeout(1000)
    return resp
}

export async function postQuestion(question) {
    const resp = await ourServer.post('question', {
        q: question
    })
    // setTimeout(1000)
    return resp.data.q
}

export async function postBackEndDBUpdate(value) {
    const resp = await ourServer.post('backend', {
        val: value
    })
    console.log(resp.status)
}