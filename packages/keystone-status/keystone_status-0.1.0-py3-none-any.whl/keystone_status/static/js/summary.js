/* Define reusable HTML templates as JQuery objects                         */
/****************************************************************************/

function statusIconTemplate(statusCode) {
  const statusIcons = {
    200: '<i class="bi bi-check-circle-fill text-success px-1"></i>',
    500: '<i class="bi bi-exclamation-octagon-fill text-danger px-1"></i>',
    null: '<i class="bi bi-question-circle-fill text-secondary px-1"></i>'
  };

  return statusIcons[statusCode] || statusIcons[null]
}

function historyListItemTemplate(statusCheck) {
  const statusStyle = {200: 'success', 500: 'danger'}[statusCheck.status] || 'secondary';
  const statusStr = statusCheck.status == 200 ? 'Operational' : 'Degraded';
  return $(`
      <li class="li-${statusStyle}">
        <div class="d-flex justify-content-between">
          <div>${statusStr} (${statusCheck.status})</div>
          <div>${statusCheck.time}</div>
        </div>
        <div>${statusCheck.message}</div>
      </li>
  `);
}

function historyListTemplate(serviceSummary) {
  const $historyList = $('<ul class="history"></ul>');
  $.each(serviceSummary.history, (index, statusCheck) => {
    $historyList.append(historyListItemTemplate(statusCheck))
  })
  return $historyList
}

function statusAccordianItemTemplate(serviceSummary) {
  const statusIcon = statusIconTemplate(serviceSummary.latest.status);
  const $accordianItem = $(`
    <div class="accordion-item my-2">
      <h3 id="heading-${serviceSummary.id}" class="accordion-header">
        <button id="heading-content-${serviceSummary.id}" class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${serviceSummary.id}" aria-expanded="true" aria-controls="collapse-${serviceSummary.id}">
          <div class="text-truncate">${statusIcon} ${serviceSummary.name}</div>
        </button>
      </h3>

      <div id="collapse-${serviceSummary.id}" class="accordion-collapse collapse" aria-labelledby="heading-${serviceSummary.id}" data-bs-parent="#statusAccordion">
        <div id="collapse-content-${serviceSummary.id}" class="accordion-body">
          <div class="d-flex justify-content-center">
            No status information is available at this time.
          </div>
        </div>
      </div>
    </div>
  `);

  // Replace the "No status information is available" message if history data is available
  if (serviceSummary.history.length) {
    const $historyList = historyListTemplate(serviceSummary)
    $accordianItem.find(`#collapse-content-${serviceSummary.id}`).html($historyList)
  }

  return $accordianItem
}

function statusAccordianTemplate(data) {
  const $statusAccordian = $('<div id="statusAccordion" class="accordion"></div>')
  $.each(data, (index, value) => {
    $statusAccordian.append(statusAccordianItemTemplate(value));
  })
  return $statusAccordian
}

function statusCardTemplate(data) {
  const is200 = data.every(function (obj) {
    return obj.latest.status == 200;
  });

  const $card = $('<div>', {class: "card my-5"});
  const $cardBody = $('<div>', {class: "card-body fs-5"});
  $card.append($cardBody)

  if (is200) {
    $card.addClass("bg-success")
    $cardBody.html('<i class="bi bi-check-circle-fill text-white px-1"></i> All Systems Online');
  } else {
    $card.addClass("bg-warning")
    $cardBody.html('<i class="bi bi-exclamation-triangle-fill text-white px-1"></i> System Status Degraded');
  }
  return $card
}

function pageHeaderTemplate() {
  return $(`
    <div class="my-5 py-4 text-center">
      <h1 class="">Keystone Status</h1>
    </div>
  `)
}

/* Fetch API data and populate the page                                     */
/****************************************************************************/

$(document).ready(function () {
  const $contentDiv = $('#content')
  $.getJSON(window.location.origin + "/api/summary", (data) => {
    $contentDiv.append(pageHeaderTemplate())
    $contentDiv.append(statusCardTemplate(data))
    $contentDiv.append('<h3 class="my-4">Health Checks</h3>')
    $contentDiv.append(statusAccordianTemplate(data))
  })
});
