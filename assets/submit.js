function validate_link(event) {
    text = document.getElementById("discordlink").value

    if (text == "") {
        document.getElementById("link-msg").innerText = "Message link is required"
        window.valid_link = false;
        return
    }

    sections = text.split("/")

    if (sections[0] != "https:" && sections[0] != "http:") {
        document.getElementById("link-msg").innerText = "Not a URL"
        window.valid_link = false;
        return
    }
    if (!["discord.com", "canary.discord.com", "ptb.discord.com"].includes(sections[2])) {
        document.getElementById("link-msg").innerText = "Not a Discord link"
        window.valid_link = false;
        return
    }
    if (sections[3] != "channels") {
        document.getElementById("link-msg").innerText = "Wrong type of discord link"
        window.valid_link = false;
        return
    }

    if (!isNumeric(sections[4]) || !isNumeric(sections[5]) || !isNumeric(sections[6])) {
        document.getElementById("link-msg").innerText = "Invalid link."
        window.valid_link = false;
        return
    }

    window.currentMessageID = sections[6]

    fetch("/existing_url?messageid=" + window.currentMessageID, {
        method: "GET",
    }).then(res => {
        if (res.status === 200) {
            document.getElementById("link-msg").innerText = "Valid Link"
            window.valid_link = true;
        } else {
            window.currentMessageID = null;
            window.valid_link = false;
            document.getElementById("link-msg").innerText = "A message with that ID already exists"
        }
    })
}

function isNumeric(value) {
    return /^-?\d+$/.test(value);
}

window.onload = () => {
    validate_link()
}

function submit() {
    if (!window.valid_link) {
        alert("The link is invalid!")
        return
    }

    fetch("/submit_new", {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({
            "category": document.getElementById("category").value,
            "messageid": window.currentMessageID,
            "messagetext": document.getElementById("msgtext").value,
            "token": browserid()
        })
    }).then((res) => {
        if (res.status === 200) {
            alert("Success!")

            document.getElementById("msgtext").value = ""
            document.getElementById("discordlink").value = ""
        } else {
            res.text().then((text) => {
                alert("Something went wrong: " + text)
            })
        }
    })
}

function browserid() {
    if (localStorage.getItem("lowqualitytrollprevention")) {
        return localStorage.getItem("lowqualitytrollprevention")
    } else {
        token = navigator.userAgent.toLowerCase() + "@@" + navigator.language + "@@" + (Math.random() + 1).toString(36).substring(7)
        token = btoa(token)
        localStorage.setItem("lowqualitytrollprevention", token)

        return token
    }
}

function check_for_keywords() {
    text = document.getElementById("msgtext").value
    categories_flagged = []

    for (const [name, words] of Object.entries(window.keywords)) {
        if (name !== document.getElementById("category").value) {
            for (const entry of words) {
                if (text.toLowerCase().includes(entry.toLowerCase())) {
                    categories_flagged.push(name)
                    break
                }
            }
        }
    }

    if (categories_flagged.length > 0) {
        text = "Are you sure your category is correct? Keywords connected to:<ul>"
        for (const name of categories_flagged) {
            text = text + "<li>" + name + "</li>"
        }

        document.getElementById("warning_message").innerHTML = text + "</ul> have been found"
    } else {
        document.getElementById("warning_message").innerHTML = ""
    }
}

fetch("/get_keywords", {
    method: "GET"
}).then((res) => {
    res.json().then((res) => {
        window.keywords = res
    })
})