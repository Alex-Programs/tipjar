window.onload = () => {
    fetch("/list.json", {
        method: "GET"
    }).then(res => res.json())
        .then(res => {
            window.tips = res["categories"]

            renderTips()
        })
}

function renderTips() {
    rawTips = []

    for (const category of window.tips) {
        for (const tip of category["tips"]) {
            tip["category"] = category["name"]
            rawTips.push(tip)
        }
    }

    rawTips.sort((a, b) => {
        return a["time"] - b["time"]
    }).reverse()

    console.log(rawTips)

    rawTips.forEach((tip) => {
        row = document.createElement("tr")

        uid = document.createElement("td")
        uid.innerText = tip["uid"]

        category = document.createElement("td")
        category.innerText = tip["category"]

        messageid = document.createElement("td")
        messageid.innerText = tip["messageid"]

        time = document.createElement("td")
        time.innerText = new Date(tip["time"] * 1000).toLocaleString()

        text = document.createElement("td")
        text.innerText = tip["text"]

        link = document.createElement("td")

        try {
            link.innerText = tip["link"]
        } catch (e) {
            link.innerText = "None"
        }

        row.appendChild(uid)
        row.appendChild(category)
        row.appendChild(messageid)
        row.appendChild(time)
        row.appendChild(text)
        row.appendChild(link)

        document.getElementById("tipsTable").appendChild(row)
    })
}

function delete_by_id(uid) {
    fetch("/admin_delete", {
        method: "POST",
        body: JSON.stringify({"uid": uid})
    }).then((res) => {
        window.location.reload()
    })
}