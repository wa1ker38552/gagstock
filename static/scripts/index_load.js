function renderUpdate(ver, titles, content) {
    const e = dcreate("div", "update", `
    <h4 style='font-family: "Fira Code"'>${ver}</h4>
    ${titles.length != 0 ? `<div class='gap'></div>
    <h3>${titles.join(", ")}</h3>`: ''}
    `)
    const md = dcreate("div")
    md.innerHTML = marked.parse(content.join('\n'))
    e.append(md)
    twemoji.parse(e, {
        folder: 'svg',
        ext: '.svg',
        base: 'https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/'
    })
    return e
}


window.onload = function() {
    const updateContainer = dquery("#updateContainer")
    request("/api/updates")
        .then(updates => {
            for (u of updates.slice(0, 5)) {
                split = u.content.split('\n')
                v = split[0].replace("Update ", "")
                titles = []
                content = []
                for (line of split.slice(1)) {
                    if (line.trim()[0] == "#") {
                        if (!line.toLowerCase().includes("play now")) {
                            titles.push(line.replaceAll("#", "").trim())
                        }
                    } else if (line.trim() != "" && !line.toLowerCase().includes("@everyone")) {
                        content.push(line.trim())
                    }
                }
                updateContainer.append(renderUpdate(v, titles, content))
                dquery("#loadingScreen").remove()
            }
        })
}