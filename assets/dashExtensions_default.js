window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(e) {
            window.open(e.target.href, '_blank');
        }
    }
});