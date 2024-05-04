/*
 * The internal definitions
 *
 * Copyright (C) 2023-2024, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( _LIBVSBSDL_INTERNAL_DEFINITIONS_H )
#define _LIBVSBSDL_INTERNAL_DEFINITIONS_H

#include <common.h>

/* Define HAVE_LOCAL_LIBVSBSDL for local use of libvsbsdl
 */
#if !defined( HAVE_LOCAL_LIBVSBSDL )
#include <libvsbsdl/definitions.h>

/* The definitions in <libvsbsdl/definitions.h> are copied here
 * for local use of libvsbsdl
 */
#else
#define LIBVSBSDL_VERSION			20240504

/* The libvsbsdl version string
 */
#define LIBVSBSDL_VERSION_STRING		"20240504"

/* The endian definitions
 */
#define LIBVSBSDL_ENDIAN_BIG			_BYTE_STREAM_ENDIAN_BIG
#define LIBVSBSDL_ENDIAN_LITTLE			_BYTE_STREAM_ENDIAN_LITTLE

/* The access flags definitions
 * bit 1        set to 1 for read access
 * bit 2        set to 1 for write access
 * bit 3-8      not used
 */
enum LIBVSBSDL_ACCESS_FLAGS
{
	LIBVSBSDL_ACCESS_FLAG_READ		= 0x01,
/* Reserved: not supported yet */
	LIBVSBSDL_ACCESS_FLAG_WRITE		= 0x02
};

/* The file access macros
 */
#define LIBVSBSDL_OPEN_READ			( LIBVSBSDL_ACCESS_FLAG_READ )
/* Reserved: not supported yet */
#define LIBVSBSDL_OPEN_WRITE			( LIBVSBSDL_ACCESS_FLAG_WRITE )
/* Reserved: not supported yet */
#define LIBVSBSDL_OPEN_READ_WRITE		( LIBVSBSDL_ACCESS_FLAG_READ | LIBVSBSDL_ACCESS_FLAG_WRITE )

#endif /* !defined( HAVE_LOCAL_LIBVSBSDL ) */

#define LIBVSBSDL_MAXIMUM_CACHE_ENTRIES_SECTORS	16

#endif /* !defined( _LIBVSBSDL_INTERNAL_DEFINITIONS_H ) */

