/* 
 * The scanner for sia description language
 *
 * @file    sia2graph.lex
 * @author  Simon Maurer
 *
 * */

%{
    #include <stdio.h>
    #include "sia2graph.tab.h"  // to get the token types that we return
    #define YY_DECL extern int yylex()
    extern int yyerror( void*, const char* );
%}
%option noinput
%option nounput
%option yylineno

%x comment
%%
    /* skip whitespaces and CR */
[ \t]           ;
\n              ++yylloc.last_line;

    /* ignore comments */
"/*"         BEGIN(comment);

<comment>[^*\n]*        /* eat anything that's not a '*' */
<comment>"*"+[^*/\n]*   /* eat up '*'s not followed by '/'s */
<comment>\n             ++yylloc.last_line;
<comment>"*"+"/"        BEGIN(INITIAL);

"//".*          { /* DO NOTHING */ }

    /* keywords */

    /* identifiers */
[a-zA-Z_$][a-zA-Z_$0-9]* {
                yylval.sval = strdup(yytext);
                return IDENTIFIER;
}

    /* operators */
[.|!?;:]     return *yytext;

    /* anything else is an error */
.               yyerror( NULL, "invalid character" );
%%

