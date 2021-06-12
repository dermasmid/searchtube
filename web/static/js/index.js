var index = 0
var data = []
var numOfresults = 0
let searchTerm = ''



function getData(url, callback) {
    onSearch()
    fetch(url).then((resp) => {
        resp.json().then((data) => {
            document.getElementById('loading-png').remove()
            callback(data)
        })
    })
}

function onSearch() {
    index = 0
    let resultsContainer = document.getElementById('results-container')
    resultsContainer.innerHTML = ''
    // loading
    let img = document.createElement('img')
    img.id = 'loading-png'
    img.className = 'loading-png'
    img.src = 'static/images/loading.png'
    resultsContainer.appendChild(img)
    const menu = document.getElementById('menu')
    menu.innerHTML = ''
    let results = document.createElement('div')
    results.id = 'results'
    resultsContainer.appendChild(results)
    let button = document.createElement('button')
    button.innerHTML = 'Load More'
    button.className = 'load-more-button'
    resultsContainer.appendChild(button)

    button.addEventListener('click', (e) => {
        addFive()
    })
}

function displayInfo() {
    const menu = document.getElementById('menu')
    menu.style.display = 'block'
    const num = document.createElement('p')
    num.className = 'number-of-results'
    num.innerHTML = `Total results: ${data.length} | Query: ${searchTerm}`
    menu.appendChild(num)
}


function addFive() {
    for (let i = index + 5; index < i && index < numOfresults; index++) {
        results = document.getElementById('results')
        let iframe = document.createElement('iframe')
        iframe.className = 'iframe'
        if (screen.width > 750) {
            iframe.style.width = '495px'
            iframe.style.height = '280px'
        } else {
            iframe.style.width = '320px'
            iframe.style.height = '180px'
        }

        iframe.src = data[index]
        results.appendChild(iframe)
    }
    if (numOfresults == index) {
        let button = document.getElementsByClassName('load-more-button')[0]
        button.style.display = 'none'
    }
}

function handleData(rawData) {
    data = rawData.data
    numOfresults = data.length
    displayInfo()
    addFive()
}


function get_remix() {
    data = {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(data.slice(0, 4))
    }
    console.log(data)
    fetch('/compress', data).then((resp) => {
        resp.text().then((data) => {
            // window.location.href = data
        })
    })
}

function runInit() {
    if (window.location.href.includes('?q=')) {
        searchTerm = window.location.href.split('?q=')[1].replace(/%20/g, ' ')
        getData('/search?q=' + searchTerm.toLowerCase(), handleData)
    }
}

runInit()



$(document).ready(function() {
    $('select').niceSelect()

    document.getElementById('search-form').addEventListener("submit", (e) => {
        e.preventDefault();
        let q = document.getElementById('search')
        searchTerm = q.value;
        q.value = ''
        let channel = document.getElementById('channel-select')
        let channelId
        if (channel) {
            channelId = channel.value
        } else {
            channelId = 0
        }
        getData('/search?q=' + searchTerm.toLowerCase() + '&channel_id=' + channelId, handleData)
    });


  });
