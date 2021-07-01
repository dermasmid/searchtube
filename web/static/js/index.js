var index = 0
var data = []
var numOfresults = 0



function getData(url, params, callback) {
    onSearch()
    fetch(url).then((resp) => {
        resp.json().then((data) => {
            document.getElementById('loading-png').remove()
            callback(data, params)
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

function displayInfo(searchTerm) {
    const menu = document.getElementById('menu')
    menu.style.display = 'block'
    const num = document.createElement('p')
    num.className = 'number-of-results'
    num.innerText = `Total results: ${data.length} | Query: ${searchTerm}`
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

function handleData(rawData, params) {
    data = rawData.data
    numOfresults = data.length
    window.history.pushState({}, '', '/?q=' + params.term + '&channel_id=' + params.channelId);
    displayInfo(params.term)
    addFive()
}


function runInit() {
    let currentUrl = new URL(window.location.href)
    let channelId = currentUrl.searchParams.get('channel_id')
    searchTerm = currentUrl.searchParams.get('q')
    if (channelId) {
        let option = $('option[value="' + channelId + '"]').attr('selected', 'selected')
        $('select').niceSelect('update')
    }
    if (searchTerm) {
        params = getCurrentQuery()
        params.term = searchTerm
        let url = '/search?q=' + params.term + '&channel_id=' + params.channelId
        getData(url, params, handleData)
    }
}


function getCurrentQuery() {
    let q = document.getElementById('search')
    let searchTerm = q.value;
    q.value = ''
    let channel = document.getElementById('channel-select')
    let channelId
    if (channel) {
        channelId = channel.value
    } else {
        channelId = 0
    }
    let url = '/search?q=' + searchTerm.toLowerCase() + '&channel_id=' + channelId
    params = {
        term: searchTerm,
        channelId: channelId
    }
    return params
}

$(document).ready(function() {
    $('select').niceSelect()
    document.getElementById('search-form').addEventListener("submit", (e) => {
        e.preventDefault();
        params = getCurrentQuery()
        let url = '/search?q=' + params.term + '&channel_id=' + params.channelId
        getData(url, params, handleData)
    });
    runInit()
  });
