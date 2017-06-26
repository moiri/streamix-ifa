/**
 * Allows to build a graph structure from the sia parser
 *
 * @file    sia.c
 * @author  Simon Maurer
 *
 */

#include <stdlib.h> /* For malloc to add nodes to a linked list */
#include "sia.h"
#include <igraph.h>

/******************************************************************************/
sia_target_t* sia_create_target( const char* action , char mode,
        const char* state )
{
    sia_target_t* target = malloc( sizeof( struct sia_target_s ) );
    target->name = action;
    target->mode = mode;
    target->vertex = state;
    return target;
}

/******************************************************************************/
sia_targets_t* sia_add_target( sia_target_t* target, sia_targets_t* list )
{
    sia_targets_t* targets = malloc( sizeof( struct sia_targets_s ) );
    targets->target = target;
    targets->next = list;
    return targets;
}

/******************************************************************************/
sia_vertex_t* sia_create_vertex( const char* name, sia_targets_t* targets )
{
    sia_vertex_t* state = malloc( sizeof( struct sia_vertex_s ) );
    state->name = name;
    state->targets = targets;
    return state;
}

/******************************************************************************/
sia_vertices_t* sia_add_vertex( sia_vertex_t* state, sia_vertices_t* list )
{
    sia_vertices_t* states = malloc( sizeof( struct sia_vertices_s ) );
    states->vertex = state;
    states->next = list;
    return states;
}

/******************************************************************************/
void sia_check_duplicate( igraph_t* g, sia_vertices_t* sia,
        sia_vertex_t** symbols )
{
    int id;
    sia_vertex_t* state;
    while( sia != NULL ) {
        HASH_FIND_STR( *symbols, sia->vertex->name, state );
        if( state == NULL ) {
            id = igraph_vcount( g );
            igraph_add_vertices( g, 1, NULL );
            igraph_cattribute_VAS_set( g, "label", id, sia->vertex->name );
            sia->vertex->id = id;
            HASH_ADD_STR( *symbols, name, sia->vertex );
        }
        else
            printf( "ERROR: redefinition of '%s'\n", sia->vertex->name );
        sia = sia->next;
    }
}

/******************************************************************************/
void sia_check_undefined( igraph_t* g, sia_vertex_t** symbols )
{
    int id;
    sia_vertex_t* state;
    sia_vertex_t* tmp;
    sia_vertex_t* state_tgt;
    sia_targets_t* targets;
    char* label;

    HASH_ITER(hh, *symbols, state, tmp) {
        targets = state->targets;
        while( targets != NULL ) {
            HASH_FIND_STR( *symbols, targets->target->vertex, state_tgt );
            if( state_tgt == NULL ) {
                printf( "ERROR: use of undeclared identifier '%s'\n",
                        targets->target->vertex );
                targets = targets->next;
                continue;
            }
            id = igraph_ecount( g );
            igraph_add_edge( g, state->id, state_tgt->id );
            igraph_cattribute_EAS_set( g, "name", id, targets->target->name );
            igraph_cattribute_EAS_set( g, "mode", id, &targets->target->mode );
            label = malloc( strlen( targets->target->name ) + 2 );
            sprintf( label, "%s%c", targets->target->name,
                    targets->target->mode );
            igraph_cattribute_EAS_set( g, "label", id, label );
            targets = targets->next;
        }
    }
}
