var booksApp = angular.module('booksApp', [])


booksApp.controller('BodyCtrl', function($scope) {

    $scope.init = function () {
        $scope.showBooksTable();
    };

    changeStatus = function() {
        if ($scope.isShowBooksTable) {
            $scope.statusBooks = ' active';
        } else {
            $scope.statusBooks = '';
        }

        if ($scope.isShowAuthorsTable) {
            $scope.statusAuthors = ' active';
        } else {
            $scope.statusAuthors = '';
        }
    }

    $scope.showBooksTable = function() {
        $scope.isShowBooksTable = true;
        $scope.isShowAuthorsTable = false;
        changeStatus();
    }

    $scope.showAuthorsTable = function() {
        $scope.isShowBooksTable = false;
        $scope.isShowAuthorsTable = true;
        changeStatus();
    }

});

booksApp.controller('BookTableCtrl', function($scope, $http) {

    $http.get(booksListUrl).
        then(function(response) {
            $scope.books = response.data;
        });

    $scope.showAuthors = function(authors) {
        authors_list = '';
        numberAuthors = authors.length;

        authors.forEach(function(author, i) {
            authors_list += author.firstname + ' ' + author.lastname;
            if (i+1 < numberAuthors) {
                authors_list += ', ';
            }
        });
        return authors_list;
    }
});

booksApp.controller('AuthorTableCtrl', function($scope, $http) {

    $http.get(authorsListUrl).
        then(function(response) {
            $scope.authors = response.data;
        });

    $scope.showBooks = function(books) {
        books_list = '';
        numberBooks = books.length;

        books.forEach(function(book, i) {
            books_list += book.title;
            if (i+1 < numberBooks) {
                book_list += '<br>';
            }
        });
        return books_list;
    }
});