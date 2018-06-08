function initTagSuggestingField(id) {
    $(document).ready(function () {

        var $tagitField = $('#' + id);
        var $tagitFieldContainer = $tagitField.parents('.field-content');
        var $tagSuggestionsContainer = $tagitFieldContainer.find('.tag-suggestions');
        var getVisibleTagSuggestions = function () {
            return $tagSuggestionsContainer.find('.tag').filter(function() {
                return this.style['display'] !== 'none';
            });
        };

        // Add suggested tag into a tagit input on click
        // and hide it form the relevant tags area.
        $tagSuggestionsContainer.find('.tag').on('click', function(e) {
            e.preventDefault();
            var $tagSuggestion = $(e.target);

            $tagitField.tagit('createTag', $tagSuggestion.data('tag'));
        });

        $tagitField.tagit({
            // Show a suggested tag in the relevant tags area
            // when it's removed from a tagit input.
            beforeTagRemoved: function(event, ui) {
                var tagSelector = getTagSuggestionSelector(ui.tagLabel);
                $tagSuggestionsContainer.find(tagSelector).show();

                if (getVisibleTagSuggestions().length > 0) {
                    $tagSuggestionsContainer.show();
                }
            },
            // Hide a suggested tag in the relevant tags area,
            // when it's added to a tagit area.
            // This should also cover a case when user adds a tag manually.
            beforeTagAdded: function(event, ui) {
                var tagSelector = getTagSuggestionSelector(ui.tagLabel);
                var $tagSuggestion = $tagSuggestionsContainer.find(tagSelector);

                $tagSuggestion.hide();
                if (getVisibleTagSuggestions().length === 0) {
                    $tagSuggestionsContainer.hide();
                }
            },

        });
    });

    function normalizeTagLabel(tagLabel) {
        return tagLabel.replace(/^"(.*?)"$/, "$1");
    }

    function getTagSuggestionSelector(tagLabel) {
        // FIXME: Escape quotes, becase tags like "President's Letter" will fail here.
        return ".tag[data-tag='" + normalizeTagLabel(tagLabel) + "']";
    }
}
