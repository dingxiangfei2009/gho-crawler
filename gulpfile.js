/**
 * Created by dingxiangfei on 13/2/16.
 */
var
    gulp = require('gulp'),
    sass = require('gulp-sass'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat'),
    util = require('gulp-util');

gulp.task('default', ['watch', 'semantic-css', 'sass', 'javascript']);

gulp.task('semantic-css', function() {
    gulp.src([
        'assets/semantic/dist/semantic.min.css',
        'assets/semantic/dist/components/*.min.css'
    ], {
        base: '.'
    })
        .pipe(concat('base.css'))
        .pipe(gulp.dest('visualiser/static'));
    gulp.src([
        'assets/semantic/dist/themes/**/*'
    ])
        .pipe(gulp.dest('visualiser/static/themes'));
});

gulp.task('watch', function() {
    gulp.watch('visualiser/stylesheet/**/*.sass', ['sass']);
    gulp.watch('visualiser/javascript/**/*.js', ['javascript']);
});

gulp.task('sass', function() {
    gulp.src('visualiser/stylesheet/*.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('visualiser/static/visualiser'));
});

gulp.task('javascript', function() {
    gulp.src('visualiser/javascript/*.js')
        //.pipe(uglify().on('error', util.log))
        .pipe(gulp.dest('visualiser/static/visualiser'));
    gulp.src([
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/requirejs/require.js',
        'assets/semantic/dist/semantic.min.js',
        'assets/semantic/dist/components/*.min.js',
        'assets/vis/vis.js'
    ], {
        base: '.'
    })
        //.pipe(uglify().on('error', util.log))
        .pipe(concat('base.js'))
        .pipe(gulp.dest('visualiser/static'));
});