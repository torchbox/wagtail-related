function initTagSuggestingField(id) {
    $(document).on('ready', function () {
        var $tagitField = $('#' + id);
        var $tagitFieldContainer = $tagitField.parents('.js-field-content');
        var $tagSuggestionsContainer = $tagitFieldContainer.find('.js-tag-suggestions');
        var $tagSuggestionsListContainer = $tagSuggestionsContainer.find('.js-tag-suggestions--wrapper');
        var $tagRefreshButton = $tagitFieldContainer.find('.js-tag-refresh');
        var refreshURL = $tagRefreshButton.data('refresh-url');

        // Load the data first time
        loadData(refreshURL);

        $tagRefreshButton.on('click', function (e) {
            e.preventDefault();

            loadData(refreshURL);
        });

        var getVisibleTagSuggestions = function () {
            return $tagSuggestionsListContainer.find('.js-tag').filter(function() {
                return this.style['display'] !== 'none';
            });
        };

        // Add suggested tag into a tagit input on click
        // and hide it form the relevant tags area.
        $tagSuggestionsListContainer.on('click', '.js-tag', function(e) {
            e.preventDefault();
            var $tagSuggestion = $(e.target);

            $tagitField.tagit('createTag', $tagSuggestion.attr('data-tag'));
        });

        $tagitField.tagit({
            // Show a suggested tag in the relevant tags area
            // when it's removed from a tagit input.
            beforeTagRemoved: function(event, ui) {
                var tagSelector = getTagSuggestionSelector(ui.tagLabel);
                $tagSuggestionsListContainer.find(tagSelector).show();

                showOrHideTagSuggestionsContainer();
            },
            // Hide a suggested tag in the relevant tags area,
            // when it's added to a tagit area.
            // This should also cover a case when user adds a tag manually.
            beforeTagAdded: function(event, ui) {
                var tagSelector = getTagSuggestionSelector(ui.tagLabel);
                var $tagSuggestion = $tagSuggestionsListContainer.find(tagSelector);

                $tagSuggestion.hide();
                showOrHideTagSuggestionsContainer();
            },
        });

        function loadData(loadURL) {
            $.ajax(loadURL, {
                success: function (data) {
                    renderTags(data.suggested_tags);
                }
                // TODO: Handle errors
            });
        }

        function renderTags(suggestedTags) {
            var existingTags = $tagitField.tagit("assignedTags").map(function(tagLabel) {
                return normalizeTagLabel(tagLabel);
            });

            $tagSuggestionsListContainer.empty();

            suggestedTags.forEach(function (tagLabel) {
                var $htmlTag = generateHTMLForTag(tagLabel);

                if (existingTags.indexOf(tagLabel) >= 0) {
                    // If tag is already exists we need to
                    // append it, but hide
                    $htmlTag.hide();
                }
                $tagSuggestionsListContainer.append($htmlTag);
                // Insert space between tags to enable word wrap
                $tagSuggestionsListContainer.append(" ");
            });

            showOrHideTagSuggestionsContainer();
        }

        function generateHTMLForTag(tagLabel) {
            var $htmlTag = $('<span class="js-tag tag tagit-label"></span>');

            // Note that we have to use the `attr` method instead of
            // the `data` method, because we need to perform
            // selection by data attribute later.
            $htmlTag.attr('data-tag', tagLabel);
            $htmlTag.text(tagLabel);

            return $htmlTag;
        }

        function showOrHideTagSuggestionsContainer() {
            if (getVisibleTagSuggestions().length === 0) {
                $tagSuggestionsContainer.hide();
            } else {
                $tagSuggestionsContainer.show();
            }
        }
    });

    // We need to normalize tag labesl because tagit
    // returns quoted labels, if a tag has spaces
    function normalizeTagLabel(tagLabel) {
        return tagLabel.replace(/^"(.*?)"$/, "$1");
    }

    function getTagSuggestionSelector(tagLabel) {
        return ".js-tag[data-tag='" + normalizeTagLabel(tagLabel) + "']";
    }
}
