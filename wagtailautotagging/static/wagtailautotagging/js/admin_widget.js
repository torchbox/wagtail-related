function initTagSuggestingField(id) {
    $(document).on('ready', function () {
        var $tagitField = $('#' + id);
        var $tagitFieldContainer = $tagitField.parents('.field-content');
        var $tagSuggestionsContainer = $tagitFieldContainer.find('.tag-suggestions');

        $tagSuggestionsContainer.find('.tag').on('click', function(e) {
            e.preventDefault();
            var tagSuggestion = $(e.target);

            $tagitField.tagit('createTag', tagSuggestion.text());
            tagSuggestion.hide();
            if ($tagSuggestionsContainer.find('.tag:visible').length === 0) {
                $tagSuggestionsContainer.hide();
            }
        });

        $tagitField.tagit({
            beforeTagRemoved: function(event, ui) {
                var tagLabel = ui.tagLabel.replace(/^"(.*?)"$/, "$1");
                var tagSelector = ".tag[data-tag='" + tagLabel + "']";
                $tagSuggestionsContainer.find(tagSelector).show();
                $tagSuggestionsContainer.show();
            }
        });
    });
}
