import { describe, expect, it } from 'vitest'
import { sanitizeEmail, sanitizeUsername } from '@/utils/sanitization'

describe('@/utils/sanitization', () => {
    it('normalizes valid email addresses', () => {
        expect(sanitizeEmail(' USER@Example.COM ')).toBe('user@example.com')
    })

    it('rejects invalid email addresses', () => {
        expect(() => sanitizeEmail('invalid-email')).toThrow('Invalid E-mail')
    })

    it('normalizes usernames', () => {
        expect(sanitizeUsername(' Alice ')).toBe('alice')
    })
})
