// Handler to register sharing clicks with page tracking

async function record_share(shared_url, share_type) {
    // shared_url is the URL being shared
    // share_type is the type of share (twitter, linkedin...)

    if (shared_url == undefined || share_type == undefined) {
        console.log("Missing parameters")
        return false
    }

    // Compose the POST url
    share_tracking_url = "https://rf7t1ex0f9.execute-api.ap-southeast-1.amazonaws.com/pageshare"
    url = `${share_tracking_url}?share_service=${share_type}&share_url=${shared_url}`

    if (document.URL.includes('developdeploydeliver.com')) {
        // Live site
        response = await fetch(url, {method: "POST"})
        console.log(response.json())
    }
    else {
        // Local dev
        console.log(url)
    }
}
