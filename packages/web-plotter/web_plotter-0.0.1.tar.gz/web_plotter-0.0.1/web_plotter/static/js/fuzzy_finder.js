import { Fzf, extendedMatch } from "https://esm.sh/fzf";

export var fuzzy_finder_callback_lookup = new Map();
$(document).ready(function(){
	const escape_key_code = 27;
	const bracket_key_code = 219;
	const e_key_code = 69;
	const f_key_code = 70;
	const space_key_code = 32;
	const escape_key_codes = [escape_key_code, bracket_key_code];
	const open_window_key_codes = [e_key_code, space_key_code, f_key_code];
	const close_window_key_codes = [];

	var selectedIndex = 0;
	var formatted_results = [];
	var results = [];
	var virtualWindowOpen = false;
	var option_list;
	$('#searchInput').on('input focus', function(){
		const query = $('#searchInput').val();
		results = option_list.find(query).map(entry => entry.item);
		const chars = new Set(query.split(""));
		formatted_results = results.map((entry) => // make bold
			entry
			.split("")
			.map(char => chars.has(char) ? `<b style="font-weight: 900;">${char}</b>` : char)
			.join("")
		);
		renderResults();
	});

	function renderResults() {
		var resultsDiv = $('#results');
		resultsDiv.empty();
		formatted_results.forEach(function(item, index) {
			resultsDiv.append('<div class="result-item">' + item + '</div>');
		});
		resultsDiv.show();
		selectedIndex = 0; // Reset selected index
		highlightSelected();
	}

	function sendSelected(data) {
		$.ajax({
			url: '/fuzzy-selected',
			type: 'POST',
			data: {query: data},
			success: (data) => {
				if (typeof data === 'string'){
					data = [data]
				}
				if (data.length == 1){
					fuzzy_finder_callback_lookup.get(data[0])()
				} else {
					fuzzy_finder_callback_lookup.get(data[0])(data[1])
				}
			}
		});
	}
	$(document).on('keydown', function(e){
		if (virtualWindowOpen){
			if ($('#results').is(':visible')){
				if (e.keyCode === 38) { // Up arrow key
					e.preventDefault();
					selectedIndex = (selectedIndex - 1 + results.length) % results.length;
					highlightSelected();
				} else if (e.keyCode === 40) { // Down arrow key
					e.preventDefault();
					selectedIndex = (selectedIndex + 1 + results.length) % results.length;
					highlightSelected();
				} else if (e.keyCode === 13) { // Enter key
					e.preventDefault();
					if (selectedIndex >= 0 && selectedIndex < results.length) {
						sendSelected(results[selectedIndex]);
						closeVirtualWindow();
					}
				}
				// Scroll results container to selected item
				var selectedItem = $('.result-item.selected');
				if (selectedItem.length) {
					var container = $('#results');
					var containerTop = container.offset().top;
					var containerBottom = containerTop + container.height();
					var selectedItemTop = selectedItem.offset().top;
					var selectedItemBottom = selectedItemTop + selectedItem.outerHeight();
					if (selectedItemBottom > containerBottom) {
						container.scrollTop(container.scrollTop() + (selectedItemBottom - containerBottom));
					} else if (selectedItemTop < containerTop) {
						container.scrollTop(container.scrollTop() - (containerTop - selectedItemTop));
					}
				}
			}
			if (escape_key_codes.includes(e.keyCode) || close_window_key_codes.includes(e.keyCode)) {
				e.preventDefault();
				closeVirtualWindow();
			}
		} else if (escape_key_codes.includes(e.keyCode) || open_window_key_codes.includes(e.keyCode)) {
			e.preventDefault();
			openVirtualWindow();
		}
	});

	function highlightSelected() {
		$('.result-item').removeClass('selected');
		$('.result-item').eq(selectedIndex).addClass('selected');
	}

	function openVirtualWindow() {
		$('#virtual-window').addClass('open');
		virtualWindowOpen = true;
		$.ajax({
				url: '/string-to-fuzzy',
				type: 'GET',
				success: function(data) {
					option_list = new Fzf(data, {
						match: extendedMatch
					})
					$('#searchInput').focus();
				}
			});
	}

	function closeVirtualWindow() {
		$('#virtual-window').removeClass('open');
		virtualWindowOpen = false;
		$('#searchInput').val("");
	}

	$(document).on('click', '.result-item', function(){
		sendSelected($(this).text());
		closeVirtualWindow();
	});

	fuzzy_finder_callback_lookup.set('open virtual window', openVirtualWindow);
	fuzzy_finder_callback_lookup.set('close virtual window', closeVirtualWindow);
});

