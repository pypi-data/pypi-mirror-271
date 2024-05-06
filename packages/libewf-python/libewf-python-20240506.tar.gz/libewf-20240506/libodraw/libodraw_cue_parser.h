/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_LIBODRAW_CUE_SCANNER_LIBODRAW_CUE_PARSER_H_INCLUDED
# define YY_LIBODRAW_CUE_SCANNER_LIBODRAW_CUE_PARSER_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int libodraw_cue_scanner_debug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    CUE_END_OF_LINE = 258,         /* CUE_END_OF_LINE  */
    CUE_SEMI_COLON = 259,          /* CUE_SEMI_COLON  */
    CUE_2DIGIT = 260,              /* CUE_2DIGIT  */
    CUE_CATALOG_NUMBER = 261,      /* CUE_CATALOG_NUMBER  */
    CUE_ISRC_CODE = 262,           /* CUE_ISRC_CODE  */
    CUE_KEYWORD_STRING = 263,      /* CUE_KEYWORD_STRING  */
    CUE_MSF = 264,                 /* CUE_MSF  */
    CUE_STRING = 265,              /* CUE_STRING  */
    CUE_CATALOG = 266,             /* CUE_CATALOG  */
    CUE_CD_DA = 267,               /* CUE_CD_DA  */
    CUE_CD_ROM = 268,              /* CUE_CD_ROM  */
    CUE_CD_ROM_XA = 269,           /* CUE_CD_ROM_XA  */
    CUE_CD_TEXT = 270,             /* CUE_CD_TEXT  */
    CUE_CDTEXTFILE = 271,          /* CUE_CDTEXTFILE  */
    CUE_COPY = 272,                /* CUE_COPY  */
    CUE_DATAFILE = 273,            /* CUE_DATAFILE  */
    CUE_FLAGS = 274,               /* CUE_FLAGS  */
    CUE_FOUR_CHANNEL_AUDIO = 275,  /* CUE_FOUR_CHANNEL_AUDIO  */
    CUE_FILE = 276,                /* CUE_FILE  */
    CUE_INDEX = 277,               /* CUE_INDEX  */
    CUE_ISRC = 278,                /* CUE_ISRC  */
    CUE_NO_COPY = 279,             /* CUE_NO_COPY  */
    CUE_NO_PRE_EMPHASIS = 280,     /* CUE_NO_PRE_EMPHASIS  */
    CUE_POSTGAP = 281,             /* CUE_POSTGAP  */
    CUE_PRE_EMPHASIS = 282,        /* CUE_PRE_EMPHASIS  */
    CUE_PREGAP = 283,              /* CUE_PREGAP  */
    CUE_REMARK = 284,              /* CUE_REMARK  */
    CUE_TRACK = 285,               /* CUE_TRACK  */
    CUE_TWO_CHANNEL_AUDIO = 286,   /* CUE_TWO_CHANNEL_AUDIO  */
    CUE_CDTEXT_ARRANGER = 287,     /* CUE_CDTEXT_ARRANGER  */
    CUE_CDTEXT_COMPOSER = 288,     /* CUE_CDTEXT_COMPOSER  */
    CUE_CDTEXT_DISC_ID = 289,      /* CUE_CDTEXT_DISC_ID  */
    CUE_CDTEXT_GENRE = 290,        /* CUE_CDTEXT_GENRE  */
    CUE_CDTEXT_MESSAGE = 291,      /* CUE_CDTEXT_MESSAGE  */
    CUE_CDTEXT_PERFORMER = 292,    /* CUE_CDTEXT_PERFORMER  */
    CUE_CDTEXT_SIZE_INFO = 293,    /* CUE_CDTEXT_SIZE_INFO  */
    CUE_CDTEXT_SONGWRITER = 294,   /* CUE_CDTEXT_SONGWRITER  */
    CUE_CDTEXT_TITLE = 295,        /* CUE_CDTEXT_TITLE  */
    CUE_CDTEXT_TOC_INFO1 = 296,    /* CUE_CDTEXT_TOC_INFO1  */
    CUE_CDTEXT_TOC_INFO2 = 297,    /* CUE_CDTEXT_TOC_INFO2  */
    CUE_CDTEXT_UPC_EAN = 298,      /* CUE_CDTEXT_UPC_EAN  */
    CUE_REMARK_LEAD_OUT = 299,     /* CUE_REMARK_LEAD_OUT  */
    CUE_REMARK_ORIGINAL_MEDIA_TYPE = 300, /* CUE_REMARK_ORIGINAL_MEDIA_TYPE  */
    CUE_REMARK_RUN_OUT = 301,      /* CUE_REMARK_RUN_OUT  */
    CUE_REMARK_SESSION = 302,      /* CUE_REMARK_SESSION  */
    CUE_UNDEFINED = 303            /* CUE_UNDEFINED  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif
/* Token kinds.  */
#define YYEMPTY -2
#define YYEOF 0
#define YYerror 256
#define YYUNDEF 257
#define CUE_END_OF_LINE 258
#define CUE_SEMI_COLON 259
#define CUE_2DIGIT 260
#define CUE_CATALOG_NUMBER 261
#define CUE_ISRC_CODE 262
#define CUE_KEYWORD_STRING 263
#define CUE_MSF 264
#define CUE_STRING 265
#define CUE_CATALOG 266
#define CUE_CD_DA 267
#define CUE_CD_ROM 268
#define CUE_CD_ROM_XA 269
#define CUE_CD_TEXT 270
#define CUE_CDTEXTFILE 271
#define CUE_COPY 272
#define CUE_DATAFILE 273
#define CUE_FLAGS 274
#define CUE_FOUR_CHANNEL_AUDIO 275
#define CUE_FILE 276
#define CUE_INDEX 277
#define CUE_ISRC 278
#define CUE_NO_COPY 279
#define CUE_NO_PRE_EMPHASIS 280
#define CUE_POSTGAP 281
#define CUE_PRE_EMPHASIS 282
#define CUE_PREGAP 283
#define CUE_REMARK 284
#define CUE_TRACK 285
#define CUE_TWO_CHANNEL_AUDIO 286
#define CUE_CDTEXT_ARRANGER 287
#define CUE_CDTEXT_COMPOSER 288
#define CUE_CDTEXT_DISC_ID 289
#define CUE_CDTEXT_GENRE 290
#define CUE_CDTEXT_MESSAGE 291
#define CUE_CDTEXT_PERFORMER 292
#define CUE_CDTEXT_SIZE_INFO 293
#define CUE_CDTEXT_SONGWRITER 294
#define CUE_CDTEXT_TITLE 295
#define CUE_CDTEXT_TOC_INFO1 296
#define CUE_CDTEXT_TOC_INFO2 297
#define CUE_CDTEXT_UPC_EAN 298
#define CUE_REMARK_LEAD_OUT 299
#define CUE_REMARK_ORIGINAL_MEDIA_TYPE 300
#define CUE_REMARK_RUN_OUT 301
#define CUE_REMARK_SESSION 302
#define CUE_UNDEFINED 303

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{

        /* The numeric value
         */
        uint32_t numeric_value;

        /* The string value
         */
	struct cue_string_value
	{
		/* The string data
		 */
	        const char *data;

		/* The string length
		 */
		size_t length;

	} string_value;


};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE libodraw_cue_scanner_lval;


int libodraw_cue_scanner_parse (void *parser_state);


#endif /* !YY_LIBODRAW_CUE_SCANNER_LIBODRAW_CUE_PARSER_H_INCLUDED  */
