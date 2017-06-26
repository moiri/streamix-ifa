/**
 * Allows to build a graph structure from the sia parser
 *
 * @file    sia.h
 * @author  Simon Maurer
 *
 */

#ifndef SIA_H
#define SIA_H

#include "uthash.h"
#include "igraph.h"

// TYPEDEFS -------------------------------------------------------------------
typedef struct sia_vertex_s sia_vertex_t;
typedef struct sia_vertices_s sia_vertices_t;
typedef struct sia_target_s sia_target_t;
typedef struct sia_targets_s sia_targets_t;

// STRUCTS --------------------------------------------------------------------
/**
 * @brief State structure of a SIA
 */
struct sia_vertex_s
{
    const char*     name;       /**< name of the state (hash key) */
    int             id;         /**< id number of the state */
    sia_targets_t*  targets;    /**< ::sia_targets_s */
    UT_hash_handle  hh;         /**< makes this structure hashable */
};

/**
 * @brief List of state structures of a SIA
 */
struct sia_vertices_s
{
    sia_vertex_t*   vertex;     /**< ::sia_vertex_s */
    sia_vertices_t* next;       /**< ::sia_vertices_s, pointer to next elem */
};

/**
 * @brief Target of a SIA state
 */
struct sia_target_s
{
    const char*     name;       /**< name of the action */
    char            mode;       /**< mode of the action */
    const char*     vertex;     /**< name of target state */
};

/**
 * @brief List of target structures of a SIA state
 */
struct sia_targets_s
{
    sia_target_t*   target;     /**< ::sia_target_s */
    sia_targets_t*  next;       /**< ::sia_targets_s, pointer to next elem */
};

// FUNCTIONS ------------------------------------------------------------------
/**
 * @brief   Create and return a target structure.
 *
 * @param const char*       name of the action
 * @param char              mode of the action
 * @param const char*       name of the target state
 * @return sia_target_t*    pointer to the created structure
 */
sia_target_t* sia_create_target( const char*, char, const char* );

/**
 * @brief   Add a target structure to a target list and return list structure.
 *
 * @param sia_target_t*     pointer to the target structure to add
 * @param sia_targets_t*    pointer to the target list the target is added
 * @return sia_targets_t*   pointer to the list structure
 */
sia_targets_t* sia_add_target( sia_target_t*, sia_targets_t* );

/**
 * @brief   Create and return a state structure.
 *
 * @param const char*       name of the state
 * @param sia_targets_t*    pointer to the a list of targets
 * @return sia_vertex_t*    pointer to the created structure
 */
sia_vertex_t* sia_create_vertex( const char*, sia_targets_t* );

/**
 * @brief   Add a state structure to a list of states and return list structure.
 *
 * @param sia_vertex_t*     pointer to the state structure to add
 * @param sia_vertices_t*   pointer to the list of states the state is added
 * @return sia_vertices_t*  pointer to the list structure
 */
sia_vertices_t* sia_add_vertex( sia_vertex_t*, sia_vertices_t* );

void sia_check_duplicate( igraph_t*, sia_vertices_t*, sia_vertex_t** );
void sia_check_undefined( igraph_t*, sia_vertex_t** );

#endif /* SIA_H */
