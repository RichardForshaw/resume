// Javascript file to get popularity stats from the blog API

// A function to
function to_blog_list_entry(page_pair, views) {
    // Try to format in the style of the original blog
    header_item = `<h3 class="blog-post-title"><a href="${page_pair[0]}">${page_pair[1]} (${views})</h3>`
    return `<tr><td>${header_item}</a></td></tr>`
}

function get_page_views() {
    const COMPARE_LENGTH = 30

    // Make a map of all the pages listed on this page
    page_map = new Map()
    $.map($(".blog-post-title a"), item => page_map.set(item.href.slice(-COMPARE_LENGTH), [item.href, item.text]))

    // Fetch data with fetch
    fetch("https://rf7t1ex0f9.execute-api.ap-southeast-1.amazonaws.com/pagetotals")
    .then( (response) => {
        // Weird that this function returns a promise...
        return response.json()
    }).then((result) => {
        console.log(result);

        // Extract top 5 pages from results
        isBlogPage = i => i[0].startsWith("blog/")
        top5_pages = Object.entries(result).filter(isBlogPage).sort((a, b) => b[1] - a[1]).slice(0,5)

        // Format and add to page
        top5_html = top5_pages.map(i => to_blog_list_entry(page_map.get(i[0].slice(-COMPARE_LENGTH)), i[1])).join('\n')
        $("#_popularity_table").html("<table>" + top5_html + "</table>");
    })
    .catch((error) => {
        console.error("Failed to fetch page view data.", error)
        $("#_popularity_table").html("Data not available... :(");
    })
}

$(document).ready(get_page_views())
