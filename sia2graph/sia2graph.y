/* 
 * The grammar of the sia description language
 *
 * @file    sia2graph.y
 * @author  Simon Maurer
 *
 * */

%{
/* Prologue */
    #include "sia.h"
    #include <stdio.h>
    extern int yylex();
    void yyerror ( void** sia, const char* s )
    {
        printf( "%s\n", s );
    }
%}

/* Bison declarations */
%parse-param { void** sia }
%define parse.error verbose
%define parse.lac full
%locations
%union {
    int ival;
    char cval;
    char *sval;
    struct sia_vertex_s* vval;
    struct sia_vertices_s* vsval;
    struct sia_target_s* tval;
    struct sia_targets_s* tsval;
};

%type <vval> stmt
%type <vsval> stmts
%type <vsval> sia
%type <tval> transition
%type <tsval> transition_opt
%type <cval> action_mode

/* idenitifiers */
%token <sval> IDENTIFIER

%start sia

%%
/* Grammar rules */
/* start of the grammer */

sia:
    stmts { *sia = $1; }
;

stmts:
    %empty { $$ = ( sia_vertices_t* )0; }
|   stmt stmts { $$ = sia_add_vertex( $1, $2 ); }
;

stmt:
    IDENTIFIER ':' transition transition_opt {
        $$ = sia_create_vertex( $1, sia_add_target( $3, $4 ) );
    }
;

transition:
    IDENTIFIER action_mode '.' IDENTIFIER {
        $$ = sia_create_target( $1, $2, $4 );
    }
;

transition_opt:
    %empty { $$ = ( sia_targets_t* )0; }
|   '|' transition transition_opt { $$ = sia_add_target( $2, $3 ); }
;

action_mode:
    '?' { $$ = '?'; }
|   '!' { $$ = '!'; }
|   ';' { $$ = ';'; }
;

%%
/* Epilogue */
