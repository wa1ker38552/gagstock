function renderSeed(seed) {
    return dcreate("div", "card", `
    <div class="card-header">${seed.name}</div>
    <div class="card-overlay"><h1>x${seed.stock}</h1></div>
    <img src="/proxy/${(seed.image) ? seed.image.replace('rbxassetid://', '') : ''}">
    `)
}

function renderEgg(egg) {
    return dcreate("div", "card", `
    <div class="card-header">${egg.name}</div>
    <img src="">
    `)
}

window.onload = function() {
    const seedContainer = dquery("#seedContainer")
    const gearContainer = dquery("#gearContainer")
    const eggContainer = dquery("#eggContainer")
    request("/api/data")
        .then(data => {
            dquery("#lastUpdated").textContent = `Last Updated: ${getRelativeTime(data.last_updated * 1000)}`
            for (seed of data.seed.data) {
                if (seed.stock != 0) {
                    seedContainer.append(renderSeed(seed))
                }
            }

            for (gear of data.gear.data) {
                if (gear.stock != 0) {
                    gearContainer.append(renderSeed(gear))
                }
            }
        })
}