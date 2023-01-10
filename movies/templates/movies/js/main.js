var csrftoken = '{{ csrf_token }}';
  console.log("CSRF TOKEN: ", csrftoken);

  $("#1337x-dropdown-trigger").click(() => {
    // When the accordian collapsible is clicked,
    // this function is triggered and will begin building
    // the dropdown children elements
    let mediaTitle = $(".title").html();
    torrents1337xDropdown(mediaTitle);
  });

  function handleTorrentItem(url, mediaId){
    console.log("Clicked", url)
    console.log("MediaID4Real:", mediaId)
    const torrents = async () => {
      const response = await fetch(`/download/add`, {
        method: "POST",
        body: JSON.stringify({magnet: url, mediaId: mediaId}),
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        credentials: "same-origin",
      });
      if (response.status === 204 || response.status === 200) {
        console.log("yay good things")
        // Disaply success message
        M.toast({ html: "Download added to queue", classes: "green" });
        return response.json;
      } else {
        console.log("Promise Rejected");
        M.toast({ html: "Failed to add media to queue. Fuck if I know why.", classes: "red" });
        return Promise.reject(response);
      }
    };
    torrents();
  }

  function torrents1337xDropdown(title) {
    // Fetches torrents by title and year released
    // and updates the 1337x torrent accordian
    // in the slide menu.
    const torrents = async () => {
      const response = await fetch(`/torrents/1337x?title=${title}`);
      const data = await response.json();
      return data;
    };
    // After torrents have been fetched from the API,
    // iterate over them and build the html list elements
    // for the accordian dropdown.
    torrents().then((data) => {
      let torrent_html = "";
      data.map((torrent) => {
        if (torrent.title != undefined) {
          const mediaId = $(".title").attr("id");
          console.log("HandleID:", mediaId);
          let h = `
                    <li class="collection-item blue darken-4 torrent-item" onClick="handleTorrentItem('${torrent.torrent_url}', '${mediaId}')">
                      <p>${torrent.title}</p>
                      <p>Seeds: ${torrent.seeds}<span class="right">Size: ${torrent.size}</span></p>
                    </li>
                    `;
          torrent_html += h;
        }
      });
      // Update the DOM and finally open the collapsibles
      // TODO: Open currently opens both collapsibles, fix
      // by using id instead of class.
      $("#1337x-dropdown").html(torrent_html);
      $(".collapsible").collapsible("open");
    });
  }

  function infoModal(title, plot) {
    // When the info icon is clicked this function
    // will dynamically update the modal with the
    // necessary information and then display it.
    $("#info-modal-title").html(title);
    $("#info-modal-plot").html(plot);
    $(".modal").modal("open");
  }

  function setupTorrentMenu(title, mediaId) {
    // Function sets up the slide out menu by clearing any previous
    // html in the accordian dropdowns, closing the accordian and setting title.
    // This would function more seemless if I moved the clear and close logic
    // to a function that triggers when the slide menu closes.
    $("#1337x-dropdown").html();
    $(".collapsible").collapsible("close");
    $(".title").html(title);
    $(".title").attr('id', mediaId)
  }

  function addAndDownload() {
    const formData = $("form").serializeArray();
    const formObject = convertToObject(formData);
    // Step 1: Send formObject to ADD endpoint
    const torrents = async () => {
      const response = await fetch(`/add`, {
        method: "POST",
        body: JSON.stringify(formObject),
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": formObject["csrfmiddlewaretoken"],
        },
        credentials: "same-origin",
      });
      if (response.status === 204) {
        // Disaply success message
        M.toast({ html: "Movie added successfully", classes: "green" });
        return response.json;
      } else {
        console.log("Promise Rejected");
        M.toast({ html: "Failed to add Movie. Fuck if I know why.", classes: "red" });
        return Promise.reject(response);
      }
    };
    torrents();
    // Step 2: Build slider menu
    setupTorrentMenu(formObject["title"], formObject['id']);
  }
  function convertToObject(unindexedArray) {
    //   Converts a serialized array to
    // an object of key:value pairs
    indexedArray = {};
    unindexedArray.map((item) => {
      indexedArray[item["name"]] = item["value"];
    });
    return indexedArray;
  }