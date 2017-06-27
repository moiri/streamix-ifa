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
typedef struct sia_s sia_t;
typedef struct sias_s sias_t;
typedef struct sia_state_s sia_state_t;
typedef struct sia_states_s sia_states_t;
typedef struct sia_transition_s sia_transition_t;
typedef struct sia_transitions_s sia_transitions_t;
typedef enum sia_format_e sia_format_t;

/**
 * @brief graph formats of the sia
 */
enum sia_format_e
{
    FMT_GRAPHML,    /**< http://graphml.graphdrawing.org/ */
    FMT_GML         /**< https://en.wikipedia.org/wiki/Graph_Modelling_Language */
};


// STRUCTS --------------------------------------------------------------------
/**
 * @brief structure of a SIA
 */
struct sia_s
{
    char*           name;       /**< name of the SIA (hash key) */
    sia_states_t*   states;     /**< ::sia_states_s */
    sia_state_t*    symbols;    /**< ::sia_states_s */
    UT_hash_handle  hh;         /**< makes this structure hashable */
};

/**
 * @brief structure of a list of SIAs
 */
struct sias_s
{
    sia_t*  sia;        /**< ::sia_s */
    sias_t* next;       /**< ::sias_s, pointer to next elem */
};

/**
 * @brief state structure of a SIA
 */
struct sia_state_s
{
    char*               name;           /**< name of the start state (hh key) */
    int                 id;             /**< id number of the state */
    sia_transitions_t*  transitions;    /**< ::sia_transitions_s */
    UT_hash_handle      hh;             /**< makes this structure hashable */
};

/**
 * @brief List of state structures of a SIA
 */
struct sia_states_s
{
    sia_state_t*   state; /**< ::sia_state_s */
    sia_states_t*  next;  /**< ::sia_states_s, pointer to next elem */
};

/**
 * @brief transition from a SIA state to a SIA state, triggered by an action
 */
struct sia_transition_s
{
    char*       action;     /**< name of the action */
    const char* mode;       /**< mode of the action */
    char*       label;
    char*       state;      /**< name of target state */
};

/**
 * @brief List of transition structures from a SIA state
 */
struct sia_transitions_s
{
    sia_transition_t*   transition; /**< ::sia_transition_s */
    sia_transitions_t*  next;       /**< ::sia_transitions_s, pointer to next elem */
};

// FUNCTIONS ------------------------------------------------------------------
/**
 * @brief   Add a sia to a list and return the list structure.
 *
 * @param sia_t*     pointer to the sia to add
 * @param sias_t*    pointer to the list the sia is added
 * @return sias_t*   pointer to the list structure
 */
sias_t* sia_add( sia_t*, sias_t* );

/**
 * @brief   Add a state to a list of states and return the list structure.
 *
 * @param sia_state_t*      pointer to the state structure to add
 * @param sia_states_t*     pointer to the list the state is added
 * @return sia_states_t*    pointer to the list structure
 */
sia_states_t* sia_add_state( sia_state_t*, sia_states_t* );

/**
 * @brief   Add a transition to a list and return the list structure.
 *
 * @param sia_transition_t*     pointer to the transition to add
 * @param sia_transitions_t*    pointer to the list the transition is added
 * @return sia_transitions_t*   pointer to the list structure
 */
sia_transitions_t* sia_add_transition( sia_transition_t*, sia_transitions_t* );

/**
 * @brief check context of sias
 *
 * Checks for duplicate identifiers and creates a graph for each sia
 *
 * @param sias_t*       a pointer to the list of sia structures
 * @param const char*   name of the sia
 * @param sia_t**       pointer to the symbol table of sias
 */
void sia_check( sias_t*, sia_format_t, const char*, sia_t** );

/**
 * @brief check for duplicate states in a sia
 *
 * Each state definition is stored in a symbol table and for each state a
 * vertex in the sia graph is created
 *
 * @param igraph_t*     pointer to the graph
 * @param sia_states_t* pointer to the list of sia states
 * @param sia_state_t** pointer to the symbol table of states
 */
void sia_check_duplicate( igraph_t*, sia_states_t*, sia_state_t** );

/**
 * @brief check for undefined state names in a sia
 *
 * Each transition is added as an edge to the sia graph
 *
 * @param igraph_t*     pointer to the graph
 * @param sia_state_t** pointer to the symbol table of states
 */
void sia_check_undefined( igraph_t*, sia_state_t** );

/**
 * @brief   Create and return a sia structure.
 *
 * @param char*             name of the sia
 * @param sia_states_t*     pointer to a list of states
 * @return sia_t*           pointer to the created structure
 */
sia_t* sia_create( char*, sia_states_t* );

/**
 * @brief   Create and return a state structure.
 *
 * @param char*                 name of the state
 * @param sia_transitions_t*    pointer to the a list of transitions
 * @return sia_state_t*         pointer to the created structure
 */
sia_state_t* sia_create_state( char*, sia_transitions_t* );

/**
 * @brief   Create and return a transition structure.
 *
 * @param char*                 name of the action
 * @param const char*           mode of the action
 * @param char*                 name of the target state
 * @return sia_transition_t*    pointer to the created structure
 */
sia_transition_t* sia_create_transition( char*, const char*, char* );

/**
 * @brief destroy all sia structures and its corresponding sub structures
 *
 * @param sias_t*   pointer to the list of sias
 */
void sia_destroy( sias_t* );

#endif /* SIA_H */
