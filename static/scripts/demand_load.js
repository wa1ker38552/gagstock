
window.onload = function() {
    request("/api/demand")
        .then(demandData => {
            const demandContainer = dquery("#demandContainer")
            dquery("#demandLastUpdated").innerHTML = getRelativeTime(demandData.last_updated * 1000)
            for (item of demandData.data) {
                demandContainer.append(dcreate("div", "demand-item vertical-container", `
                    <h3>${item[0].replace(/\b\w/g, c => c.toUpperCase())}</h3>
                    <div class='label'>${item[2].toLocaleString()} mention(s)</div>
                    <h2>${item[1]}/10</h2>  
                `))
            }

            dquery("#loadingScreen").remove()
        })
}