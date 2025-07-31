function createIconLookups(data) {
    lookup = {}
    for (key in data) {
        if (key != "last_updated") {
            for (item of data[key].data) {
                if ("image" in item) {
                    lookup[item.name] = item.image.replace("rbxassetid://", "")
                }
            }
        }
    }
    return lookup
}

function renderItem(lookup, name, value, total) {
    name = name.split(' ').filter(i => i !== '').join(' ')
    if (name == "NUM_UPDATES") {return ''}
    if (name == "Common Egg") {value = total}
    const e = dcreate("div", "chance-item centered-children", `
        <div class='vigenette'></div>
        <h4>${name.length > 12 ? name.slice(0, 10)+'...' : name}</h4>
        <h2 class='centered-children'>${Math.round(value/total*100 * 100) / 100}%</h2>
        <img src="${name in lookup ? "/proxy/"+lookup[name] : '/static/assets/not_found.png'}">
    `)
    return e
}

function convertList(data) {
    list = []
    for (key in data) {
        list.push([key, data[key]])
    }
    list.sort((a, b) => a[1] - b[1])
    list.reverse()
    return list
}

window.onload = function() {
    request("/api/chances")
        .then(chanceData => {
            request("/api/data")
                .then(rawData => {
                    lookup = createIconLookups(rawData)
                    dquery("#chanceLastUpdated").innerHTML = getRelativeTime(chanceData.last_updated * 1000)
                    const seedContainer = dquery("#seedContainer")
                    const seedTotal = chanceData.data.SeedStock.NUM_UPDATES
                    for (item of convertList(chanceData.data.SeedStock)) {
                        seedContainer.append(renderItem(lookup, item[0], item[1], seedTotal))
                    }

                    const eggContainer = dquery("#eggContainer")
                    const eggTotal = chanceData.data.Egg.NUM_UPDATES
                    for (item of convertList(chanceData.data.Egg)) {
                        eggContainer.append(renderItem(lookup, item[0], item[1], eggTotal))
                    }

                    const gearContainer = dquery("#gearContainer")
                    const gearTotal = chanceData.data.GearStock.NUM_UPDATES
                    for (item of convertList(chanceData.data.GearStock)) {
                        gearContainer.append(renderItem(lookup, item[0], item[1], gearTotal))
                    }

                    dquery("#loadingScreen").remove()
                })
        })
}