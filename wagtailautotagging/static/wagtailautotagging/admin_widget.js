function initTagSuggestingField(id) {
    $(document).on('ready', function () {
        var $tagitField = $('#' + id);
        var $tagitFieldContainer = $tagitField.parents('.field-content');
        var $tagSuggestionsContainer = $tagitFieldContainer.find('.tag-suggestions');

        $tagSuggestionsContainer.find('.tag').on('click', function(e) {
            e.preventDefault();
            var tagSuggestion = $(e.target);

            $tagitField.tagit('createTag', tagSuggestion.text());
            tagSuggestion.remove();
            if ($tagSuggestionsContainer.find('.tag').length === 0) {
                $tagSuggestionsContainer.remove();
            }
        });
    });
}
