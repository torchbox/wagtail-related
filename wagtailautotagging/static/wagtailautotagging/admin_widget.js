function initTagSuggestingField(id) {
    $(document).on('ready', function () {
        var $tagitField = $('#' + id);
        var $tagitFieldContainer = $tagitField.parents('.field-content');

        $tagitFieldContainer.find('.tag-suggestions .tag').on('click', function(e) {
            e.preventDefault();

            $tagitField.tagit('createTag', $(e.target).text());
        });
    });
}
