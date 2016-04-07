/*!
 * Star Rating <LANG> Translations
 *
 * This file must be loaded after 'fileinput.js'. Patterns in braces '{}', or
 * any HTML markup tags in the messages must not be converted or translated.
 *
 * @see http://github.com/kartik-v/bootstrap-star-rating
 * @author Kartik Visweswaran <kartikv2@gmail.com>
 *
 * NOTE: this file must be saved in UTF-8 encoding.
 */
(function ($) {
    "use strict";
    $.fn.ratingLocales['es'] = {
        defaultCaption: '{rating}',
        starCaptions: {
            0.5: '',
            1: 'Muy malo',
            1.5: '',
            2: 'Malo',
            2.5: '',
            3: 'Regular',
            3.5: '',
            4: 'Bueno',
            4.5: '',
            5: 'Excelente'
        },
        clearButtonTitle: 'Limpiar',
        clearCaption: 'Sin calificar'
    };
})(window.jQuery);
