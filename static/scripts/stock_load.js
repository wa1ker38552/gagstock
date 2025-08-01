function formatSeconds(seconds) {
  const m = Math.floor(seconds / 60).toString().padStart(2, '0');
  const s = Math.floor(seconds % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

function renderSeedSelection(parent, data) {
    parent.innerHTML = ""
    data.data.sort((a, b) => a.cost - b.cost)
    for (item of data.data) {
        if (item.stock > 0) {
            const e = dcreate("div", "stock-item", `
            <h3>${item.name}</h3>
            <div class='centered-children'>
                <img src='/proxy/${item.image ? item.image.replace('rbxassetid://', '') : ""}'>
            </div>
            <div class='text-container'>
                <h4>Cost</h4>
                <h4>${item.cost ? item.cost.toLocaleString() : "N/A"}</h4>
                <h4>Rarity</h4>
                <h4>${item.rarity}</h4>
                <h4>Stock</h4>
                <h4>x${item.stock}</h4>
            </div>
            `)
            parent.append(e)
        }
    }

    clearInterval(timerInterval)
    dquery("#updateTimer").innerHTML = formatSeconds(timers.seed)
    timerInterval = setInterval(function() {
        dquery("#updateTimer").innerHTML = formatSeconds(timers.seed)
    }, 1000)
}

function renderGearSelection(parent, data) {
    parent.innerHTML = ""
    data.data.sort((a, b) => a.cost - b.cost)
    for (item of data.data) {
        if (item.stock > 0) {
            const e = dcreate("div", "stock-item", `
            <h3 class='centered-children'>${item.name}</h3>
            <div class='centered-children'>
                <img src='/proxy/${item.image.replace('rbxassetid://', '')}'>
            </div>
            <div class='text-container'>
                <h4>Cost</h4>
                <h4>${item.cost.toLocaleString()}</h4>
                <h4>Rarity</h4>
                <h4>${item.rarity}</h4>
                <h4>Stock</h4>
                <h4>x${item.stock}</h4>
            </div>
            `)
            parent.append(e)
        }
    }

    clearInterval(timerInterval)
    dquery("#updateTimer").innerHTML = formatSeconds(timers.gear)
    timerInterval = setInterval(function() {
        dquery("#updateTimer").innerHTML = formatSeconds(timers.gear)
    }, 1000)
}

function renderEggSelection(parent, data) {
    parent.innerHTML = ""
    data.data.sort((a, b) => a.cost - b.cost)
    for (item of data.data) {
        const e = dcreate("div", "stock-item", `
        <h3 class='centered-children'>${item.name}</h3>
        <div class='centered-children'>
            <img src='/static/assets/not_found.png'>
        </div>
        <div class='text-container'>
            <h4>Cost</h4>
            <h4>${item.cost.toLocaleString()}</h4>
            <h4>Rarity</h4>
            <h4>${item.rarity}</h4>
        </div>
        `)
        parent.append(e)
    }

    clearInterval(timerInterval)
    dquery("#updateTimer").innerHTML = formatSeconds(timers.eggs)
    timerInterval = setInterval(function() {
        dquery("#updateTimer").innerHTML = formatSeconds(timers.eggs)
    }, 1000)
}

function renderCosmeticSelection(parent, data) {
    parent.innerHTML = ""
    data.data.sort((a, b) => a.cost - b.cost)
    for (item of data.data) {
        if (item.stock > 0) {
            const e = dcreate("div", "stock-item", `
            <h3 class='centered-children'>${item.name}</h3>
            <div class='centered-children'>
                <img src='/proxy/${item.image ? item.image.replace('rbxassetid://', '') : ""}'>
            </div>
            <div class='text-container'>
                <h4>Cost</h4>
                <h4>${item.cost.toLocaleString()}</h4>
                <h4>Stock</h4>
                <h4>x${item.stock}</h4>
            </div>
            `)
            parent.append(e)
        }
    }

    clearInterval(timerInterval)
    dquery("#updateTimer").innerHTML = formatSeconds(timers.cosmetics)
    timerInterval = setInterval(function() {
        dquery("#updateTimer").innerHTML = formatSeconds(timers.cosmetics)
    }, 1000)
}

function setStockSelection(i, e) {
    try {
        dquery(".selected-tag").classList.remove("selected-tag")
        e.classList.add("selected-tag")
    } catch {}

    const parent = dquery("#stockContainer")
    if (i == 0) {
        renderSeedSelection(parent, stockData.seed)
    } else if (i == 1) {
        renderGearSelection(parent, stockData.gear)
    } else if (i == 2) {
        renderEggSelection(parent, stockData.eggs)
    } else if (i == 3) {
        renderCosmeticSelection(parent, stockData.cosmetics)
    }
}

var stockData
var timerInterval
var timers = {}
var fetching = false
window.onload = function() {
    request("/api/data")
        .then(data => {
            stockData = data
            timers = {
                seed: data.seed.timer,
                gear: data.gear.timer,
                eggs: data.eggs.timer,
                cosmetics: data.cosmetics.timer
            }
            setInterval(function() {
                for (key in timers) {
                    timers[key] --
                    if (timers[key] <= 0 && !fetching) {
                        fetching = true
                        request("/api/data")
                            .then(data => {
                                fetching = false
                                stockData = data
                                timers = {
                                    seed: data.seed.timer,
                                    gear: data.gear.timer,
                                    eggs: data.eggs.timer,
                                    cosmetics: data.cosmetics.timer
                                }
                                dquery("#lastRefreshed").innerHTML = getRelativeTime(data.last_updated * 1000)
                            })
                    }
                }
            }, 1000)
            dquery("#lastRefreshed").innerHTML = getRelativeTime(data.last_updated * 1000)
            setStockSelection(0, dquery(".selected-tag"))
            dquery("#loadingScreen").remove()
        })
}