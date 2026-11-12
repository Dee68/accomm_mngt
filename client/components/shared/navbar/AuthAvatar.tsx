"use client";
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useAuthNavigation } from '@/hooks';
import { useAuthStore } from '@/lib/stores/auth-store';
import { useMyProfile } from '@/lib/query/use-users';
import { BookMarked, CircleUser, LogOut, User, Users } from 'lucide-react';
import Link from 'next/link';
import React from 'react';

export default function AuthAvatar() {
  const { handleLogout } = useAuthNavigation();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const authUser = useAuthStore((s) => s.user);
  const { data: profile, isPending } = useMyProfile();

  // If not logged in at all, render nothing.
  if (!isAuthenticated || !authUser) return null;

  // Prefer the full profile (which has the uploaded avatar).
  // Fall back to the auth user (has avatar too, but always populated).
  // If both are loading, still show the avatar using the auth user's data.
  const avatarSrc = profile?.avatar || authUser.avatar;
  const fallbackName = profile?.full_name || authUser.full_name || '';

  return (
    <div>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Avatar className='border-pumpkin cursor-pointer border-2'>
            <AvatarImage alt={fallbackName || 'auth image'} src={avatarSrc} />
            <AvatarFallback>
              <CircleUser className='dark:text-platinum size-8' />
            </AvatarFallback>
          </Avatar>
        </DropdownMenuTrigger>
        <DropdownMenuContent className='dark:text-platinum'>
          <DropdownMenuLabel className='border-b-2'>Manage Account</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem className='auth-nav'>
            <Link href='/profile' className='flex-row-center'>
              <User className='mr-1' /> My Profile
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem className='auth-nav'>
            <Link href='/tenants' className='flex-row-center'>
              <Users className='mr-1' /> Tenants
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem className='auth-nav'>
            <Link href='/bookmark' className='flex-row-center'>
              <BookMarked className='mr-1' /> My Bookmarks
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem onClick={handleLogout} className='flex-row-center auth-nav cursor-pointer'>
            <LogOut className='mr-1' /> Log Out
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
